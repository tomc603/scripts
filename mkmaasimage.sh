#!//usr/bin/env bash

set -e

BOOTSTRAPDIR="${BOOTSTRAPDIR:-${HOME}/Development/live/base/chroot}"
WORKDIR="${WORKDIR:-${HOME}/Development/live/maas}"
SKELETONDIR="${HOME}/Development/live/maas/skeleton"

# TODO: Install simplestreams on the local host and move downloaded files into skeleton
# stage1_packages="btrfs-progs,curl,dialog,dmeventd,dmidecode,dmraid,dmsetup,e2fsprogs,edac-utils,efibootmgr,efitools,efivar,grub-common,grub-efi-amd64,grub-efi-amd64-bin,grub-pc,grub2-common,hdparm,ipmitool,ipmiutil,iproute2,iputils-ping,libnss-systemd,less,lvm2,mdadm,mtr-tiny,openssh-client,openssh-server,pciutils,psmisc,smartmontools,systemd,systemd-sysv,usbutils,util-linux,vim,xfsprogs"
stage2_packages="python-webob python-routes python-yaml python-requests nginx linux-image-generic"
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

mkdir -p ${WORKDIR}/{chroot{,/boot/efi},image/live,output,scratch}
apt-get -y install debootstrap grub-pc-bin grub-efi-amd64-bin systemd-container


#
# Bootstrap a minimal Ubuntu system, including a custom package selection
#
echo "Copying bootstrap environment.."
# debootstrap --arch=amd64 --components=${stage1_components} --include=${stage1_packages} bionic ${WORKDIR}/chroot http://brutus.home.tomcameron.net/ubuntu
cp --reflink=auto -a ${BOOTSTRAPDIR}/* ${WORKDIR}/chroot/
echo "Bootstrapping finished."

# Set a default hostname and resolver
echo "buildbot" > ${WORKDIR}/chroot/etc/hostname
mkdir -p ${WORKDIR}/chroot/run/systemd/resolve
rm ${WORKDIR}/chroot/etc/resolv.conf
echo -e "nameserver 192.168.1.11\nnameserver 192.168.1.12" > ${WORKDIR}/chroot/etc/resolv.conf


#
# Install packages inside the chroot environment
#
echo "Running stage 2"

# Execute second stage inside chroot environment
cat <<EOF > ${WORKDIR}/chroot/stage2.sh
apt-get update
apt-get -y install --no-install-recommends ${stage2_packages[@]}
apt-get -y install maas maas-enlist
apt-get clean

/bin/systemctl disable smartd
/bin/systemctl enable systemd-networkd
/bin/systemctl enable systemd-resolved
/bin/systemctl enable systemd-networkd-wait-online

/usr/bin/passwd root
ssh-keygen -C "Buildbot SSH Key" -f /root/.ssh/id_ed25519 -t ed25519 -q -P ""

EOF

chmod +x ${WORKDIR}/chroot/stage2.sh
systemd-nspawn --as-pid2 -D ${WORKDIR}/chroot /stage2.sh

if [[ $? -ne 0 ]]; then
    echo "ERROR: chroot exited with a fail status"
    exit 1
fi

# Copy the skeleton directory to the chroot directory
echo "Copying skeleton directories"
cp --reflink=auto -a ${SKELETONDIR}/* ${WORKDIR}/chroot/
ln -sf /run/systemd/resolve/stub-resolv.conf ${WORKDIR}/chroot/etc/resolv.conf

# Clean up unnecessary files
# TODO: Remove unnecessary /lib/firmware entries
echo "Cleaning up unnecessary files"
rm ${WORKDIR}/chroot/stage2.sh
rm -rf ${WORKDIR}/chroot/usr/share/man/?? ${WORKDIR}/chroot/usr/share/man/??_*
rm -rf ${WORKDIR}/chroot/usr/share/locale/?? ${WORKDIR}/chroot/usr/share/locale/??_*
rm -rf ${WORKDIR}/chroot/usr/share/doc/*
rm -f ${WORKDIR}/chroot/var/lib/apt/lists/*{Packages,Release*}

cat <<'EOF' >${WORKDIR}/chroot/boot/grub/grub.cfg

insmod all_video
insmod gzio
insmod part_gpt
insmod ext2
set default="0"
set timeout=10

menuentry "Buildbot - ${timestamp}" {
    search --no-floppy --label --set=root Buildbot_Root
    linux /vmlinuz root=LABEL=Buildbot_Root ro
    initrd /initrd.img
}

menuentry "Buildbot Rescue - ${timestamp}" {
    search --no-floppy --label --set=root Buildbot_Root
    linux /vmlinuz root=LABEL=Buildbot_Root ro single nomodeset
    initrd /initrd.img
}

menuentry "System setup" {
    fwsetup
}

EOF

# This file is used by GRUB2 to find the "root" device automatically
touch ${WORKDIR}/chroot/BUILDBOT_ROOT
