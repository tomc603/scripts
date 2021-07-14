#!/usr/bin/env bash

set -e
# shopt -s nullglob

declare BASEDIR="${BASEDIR:-/mnt/storage/tom/development/work/live}"
declare WORKDIR="${WORKDIR:-${BASEDIR}/maas}"
declare SKELETONDIR="${SKELETONDIR:-${WORKDIR}/skeleton}"
declare MIRROR_ARCH="amd64"
declare MIRROR_RELEASE="xenial,xenial-security,xenial-updates,bionic,bionic-security,bionic-updates"
declare MIRROR_SECTION="main,restricted" #,universe,multiverse
declare MIRROR_SRC="rhodes.home.tomcameron.net"
declare MIRROR_DST="${MIRROR_DST:-${SKELETONDIR}/var/www/mirror/ubuntu}"
declare MIRROR_OPTS="--nosource --no-check-gpg -v --exclude-deb-section=kde --exclude-deb-section=gnome --exclude-deb-section=x11 --exclude-deb-section=games --exclude-deb-section=unity --exclude-deb-section=xfce --exclude-deb-section=translations --exclude-deb-section=otherosfs --exclude-deb-section=news --exclude-deb-section=localization --exclude-deb-section=doc --exclude-deb-section=debug --exclude-deb-section=cli-mono --exclude='/firefox' --exclude='/linux-aws' --exclude='/linux-azure' --exclude='/linux-ec2' --exclude='/linux-gcp' --exclude='/linux-linaro' --exclude='/linux-oracle' --exclude='libreoffice*' --exclude='linux-meta-oracle*' --exclude='linux-meta-gcp*' --exclude='linux-meta-azure*' --exclude='linux-meta-aws*' --exclude='linux-meta-ec2*' --exclude='linux-oem*' --exclude='linux-meta-oem*' --exclude='linux-restricted-modules-aws*' --exclude='linux-restricted-modules-azure*' --exclude='linux-restricted-modules-gcp*' --exclude='linux-restricted-modules-oem*' --exclude='linux-restricted-modules-oracle*' --exclude='linux-signed-azure*' --exclude='linux-signed-gcp*' --exclude='linux-signed-oem*' --exclude='linux-signed-oracle*' --exclude='language-support*' --exclude='mozilla*' --exclude='openoffice\.org*' --exclude='xen*'"
declare MIRROR_PROTO="http"

declare timestamp=$(date '+%Y%m%d-%H%M')


#
# Set up pre-requisites
#
if [[ ! -d ${SKELETONDIR} ]]; then
    echo "ERROR: Skeleton directory does not exist."
    exit 1
fi

if ! mkdir -p ${MIRROR_DST}; then
    echo "Unable to create mirror destination."
    exit 1
fi

apt-get -y install debmirror


#
# Mirror the package repository
#
echo "Updating mirror..."
if debmirror -a ${MIRROR_ARCH} -d ${MIRROR_RELEASE} --method ${MIRROR_PROTO} -h ${MIRROR_SRC} -s ${MIRROR_SECTION} ${MIRROR_OPTS} ${MIRROR_DST}; then
    echo "Mirror update finished."
    touch ${MIRROR_DST}/updated.${timestamp}
else
    echo "Mirror update failed!"
    touch ${MIRROR_DST}/failed.${timestamp}
    exit 1
fi

