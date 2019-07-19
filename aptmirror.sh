#!/usr/bin/env bash

set -e

declare scriptname=$(basename $0)
declare configfile="/etc/${scriptname%.sh}.conf"
declare lockfile="/var/run/${scriptname%.sh}.running"
declare logfile="/var/log/${scriptname%.sh}.log"
declare mirror="rsync://rsync.archive.ubuntu.com/ubuntu"
declare target_path="/mnt/external/mirror/ubuntu"

if [[ ! -f ${configfile} ]]; then
    echo "${scriptname}: Config file missing. Exiting." >&2
    exit 1
fi

. ${configfile}

if [[ -f ${lockfile} && $(kill -0 $(cat ${lockfile} 2> /dev/null) 2> /dev/null) ]]; then
    echo "${scriptname}: Script is already running. Exiting." >&2
    exit 2
fi

exec >> ${logfile} 2>&1

if [[ -z ${target_path} ]]; then
    echo "${scriptname}: No TARGET_PATH value defined in config file. Exiting." >&2
    exit 2
fi

trap 'rm -f ${lockfile} &> /dev/null; savelog -c 30 -n ${logfile} > /dev/null' EXIT

echo "$$" > ${lockfile} && echo "${scriptname}: Created lock file for PID $(cat ${lockfile})."

echo "${scriptname}: Starting phase 1 sync at ${EPOCHSECONDS}"
rsync -av --partial --delete --delete-after --timeout=60 \
    --exclude "indices/" \
    --exclude "dists/" \
    --exclude "project/trace/${HOSTNAME}" \
    --exclude binary-i386/ \
    --exclude daily-installer-i386/ \
    --exclude installer-i386/ \
    --exclude *_i386.deb \
    --exclude *_i386.udeb \
    --exclude Contents-i386.gz \
    --exclude binary-powerpc/ \
    --exclude daily-installer-powerpc/ \
    --exclude installer-powerpc/ \
    --exclude *_powerpc.deb \
    --exclude *_powerpc.udeb \
    --exclude Contents-powerpc.gz \
    --exclude binary-sparc/ \
    --exclude daily-installer-sparc/ \
    --exclude installer-sparc/ \
    --exclude *_sparc.deb \
    --exclude *_sparc.udeb \
    --exclude Contents-sparc.gz \
    ${mirror} ${target_path}

if [[ $? -ne 0 ]]; then
    echo "${scriptname}: Phase 1 sync failed. Exiting." >&2
    exit 3
fi
echo "${scriptname}: Completed phase 1 sync at ${EPOCHSECONDS}"

echo "${scriptname}: Starting phase 2 sync at ${EPOCHSECONDS}"
rsync -av --partial --delete --delete-after --timeout=60 \
    --exclude "pool/" \
    --exclude "project/trace/${HOSTNAME}" \
    --exclude binary-i386/ \
    --exclude daily-installer-i386/ \
    --exclude installer-i386/ \
    --exclude *_i386.deb \
    --exclude *_i386.udeb \
    --exclude Contents-i386.gz \
    --exclude binary-powerpc/ \
    --exclude daily-installer-powerpc/ \
    --exclude installer-powerpc/ \
    --exclude *_powerpc.deb \
    --exclude *_powerpc.udeb \
    --exclude Contents-powerpc.gz \
    --exclude binary-sparc/ \
    --exclude daily-installer-sparc/ \
    --exclude installer-sparc/ \
    --exclude *_sparc.deb \
    --exclude *_sparc.udeb \
    --exclude Contents-sparc.gz \
    ${mirror} ${target_path}

if [[ $? -ne 0 ]]; then
    echo "${scriptname}: Phase 2 sync failed. Exiting." >&2
    exit 3
fi
echo "${scriptname}: Completed phase 2 sync at ${EPOCHSECONDS}"

echo "${scriptname}: Cleaning up soft links."
find "${target_path}" -type l -xtype l -exec rm '{}' +

echo "${scriptname}: Removing lock file."
rm -f "${lockfile}" >& /dev/null

echo "${scriptname}: Stamping trace file."
date -u > "${target_path}/project/trace/${HOSTNAME}"

echo "${scriptname}: Sync complete."
