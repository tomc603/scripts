#!//usr/bin/env bash

set -e

WORKDIR="${WORKDIR:-${HOME}/Development/live/sysutils}"
SKELETONDIR="${HOME}/Development/live/sysutils/skeleton"
stage1_components="main,restricted,universe,multiverse"
stage1_packages="btrfs-progs,curl,dmeventd,dmidecode,dmraid,dmsetup,e2fsprogs,edac-utils,efibootmgr,efitools,efivar,grub-common,grub-efi-amd64,grub-efi-amd64-bin,grub-pc,grub2-common,hdparm,ipmitool,ipmiutil,iproute2,iputils-ping,libnss-systemd,less,lvm2,mdadm,mtr-tiny,openssh-client,openssh-server,pciutils,psmisc,smartmontools,systemd,systemd-sysv,usbutils,util-linux,vim,xfsprogs"
stage2_packages="linux-image-generic live-boot"
timestamp=$(date '+%Y%m%d-%H%M')

#
# Set up pre-requisites
#
if [[ -d ${WORKDIR}/chroot ]]; then
    echo "Removing existing chroot"
    rm -rf ${WORKDIR}/chroot
    rm -rf ${WORKDIR}/image/live/filesystem.squashfs
    # Skip this so we don't remove historical versions
    # rm -f ${WORKDIR}/output/*
fi

mkdir -p ${WORKDIR}/{image/live,output,scratch}
apt-get -y install debootstrap squashfs-tools xorriso grub-pc-bin grub-efi-amd64-bin mtools


#
# Bootstrap a minimal Ubuntu system, including a custom package selection
#
echo "Bootstrapping.."
# --variant=minbase
debootstrap --arch=amd64 --components=${stage1_components} --include=${stage1_packages} bionic ${WORKDIR}/chroot http://us.archive.ubuntu.com/ubuntu
echo "Bootstrapping finished."

# Set a default hostname
echo "systemutils" > ${WORKDIR}/chroot/etc/hostname


#
# Install packages inside the chroot environment
#
echo "Running stage 2"

# Execute second stage inside chroot environment
cat <<'EOF' > ${WORKDIR}/chroot/stage2.sh
apt-get update
apt-get -y install --no-install-recommends live-boot linux-image-generic
apt-get clean

/bin/systemctl disable smartd
/bin/systemctl enable systend-networkd
/bin/systemctl enable systemd-resolved
/bin/systemctl enable systemd-networkd-wait-online.service

/usr/bin/passwd root
EOF

chmod +x ${WORKDIR}/chroot/stage2.sh
chroot ${WORKDIR}/chroot /stage2.sh

if [[ $? -ne 0 ]]; then
    echo "ERROR: chroot exited with a fail status"
    exit 1
fi
rm ${WORKDIR}/chroot/stage2.sh

# Copy the skeleton directory to the chroot directory
echo "Copying skeleton directories"
cp -r ${SKELETONDIR}/* ${WORKDIR}/chroot/

# Clean up unnecessary files
rm -rf ${WORKDIR}/chroot/usr/share/man/?? ${WORKDIR}/chroot/usr/share/man/??_*
rm -rf ${WORKDIR}/chroot/usr/share/locale/?? ${WORKDIR}/chroot/usr/share/locale/??_*
rm -rf ${WORKDIR}/chroot/usr/share/doc/*
rm -f ${WORKDIR}/chroot/var/lib/apt/lists/*{Packages,Release*}


#
# Make the utilities image
#
mksquashfs ${WORKDIR}/chroot ${WORKDIR}/image/live/filesystem.squashfs -e boot

cp ${WORKDIR}/chroot/boot/vmlinuz-* ${WORKDIR}/image/vmlinuz
cp ${WORKDIR}/chroot/boot/initrd.img-* ${WORKDIR}/image/initrd

cat <<'EOF' >${WORKDIR}/scratch/grub.cfg

search --set=root --file /SYSUTILS_ROOT

insmod all_video

set default="0"
set timeout=10

menuentry "System Utilities - ${timestamp}" {
    linux /vmlinuz boot=live nomodeset
    initrd /initrd
}
EOF

# This file is used by GRUB2 to find the "root" device automatically
touch ${WORKDIR}/image/SYSUTILS_ROOT

# Create a GRUB2 EFI bootloader
grub-mkstandalone --format=x86_64-efi --output=${WORKDIR}/scratch/bootx64.efi \
--locales="" --fonts="" "boot/grub/grub.cfg=${WORKDIR}/scratch/grub.cfg"

# Create an EFI System Partition (ESP) image
dd if=/dev/zero of=${WORKDIR}/scratch/efiboot.img bs=1M count=10 && \
mkfs.vfat ${WORKDIR}/scratch/efiboot.img && \
mmd -i ${WORKDIR}/scratch/efiboot.img efi efi/boot && \
mcopy -i ${WORKDIR}/scratch/efiboot.img ${WORKDIR}/scratch/bootx64.efi ::efi/boot/

# Create a GRUB2 BIOS boot image
grub-mkstandalone --format=i386-pc --output=${WORKDIR}/scratch/core.img \
--install-modules="linux normal iso9660 biosdisk memdisk search tar ls" \
--modules="linux normal iso9660 biosdisk search" \
--locales="" --fonts="" "boot/grub/grub.cfg=${WORKDIR}/scratch/grub.cfg"

# Concatenate the GRUB2 ISO bootloader and BIOS boot image
cat /usr/lib/grub/i386-pc/cdboot.img ${WORKDIR}/scratch/core.img > ${WORKDIR}/scratch/bios.img

# Create a Hybrid mode ISO image with BIOS and UEFI boot support
xorriso -as mkisofs -iso-level 3 -full-iso9660-filenames \
-volid "SYSUTILS_${timestamp}" -publisher "Fastly, Inc." -preparer "Tom Cameron" \
-eltorito-boot boot/grub/bios.img -no-emul-boot -boot-load-size 4 \
-boot-info-table --eltorito-catalog boot/grub/boot.cat --grub2-boot-info \
--grub2-mbr /usr/lib/grub/i386-pc/boot_hybrid.img -eltorito-alt-boot -e EFI/efiboot.img \
-no-emul-boot -append_partition 2 0xef ${WORKDIR}/scratch/efiboot.img \
-output "${WORKDIR}/output/sysutils-${timestamp}.iso" -graft-points \
"${WORKDIR}/image" /boot/grub/bios.img=${WORKDIR}/scratch/bios.img \
/EFI/efiboot.img=${WORKDIR}/scratch/efiboot.img
