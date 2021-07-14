#!/usr/bin/env bash

set -e

declare SOURCE="/home/tom/silesia"
declare DEST="/mnt/storage/Backups/testing"
declare -i data_size=0

# Cleanup and prep
echo "Cleaning up previous runs..."
rm -rf ${DEST}/*
echo "Creating new environment"
mkdir ${DEST}/{none,lzo,zlib,zstd1,zstd3}
btrfs property set ${DEST}/none compression none
btrfs property set ${DEST}/lzo compression lzo
btrfs property set ${DEST}/zlib compression zlib
btrfs property set ${DEST}/zstd1 compression zstd:1
btrfs property set ${DEST}/zstd3 compression zstd:3

# Write tests
for dest in /mnt/storage/Backups/testing/*; do
    echo -e "\nCopying to $(basename ${dest})"
    time (for run in {1..10}; do echo "Copy ${run}"; mkdir ${dest}/${run}; cp ${SOURCE}/* ${dest}/${run}/; sync; done)
    compsize -b ${dest}
done

echo "Dropping cache..."
sync
btrfs filesystem sync ${DEST}
echo 3 > /proc/sys/vm/drop_caches

# Read tests
for dest in /mnt/storage/Backups/testing/*; do
    echo -e "\nReading from $(basename ${dest})"
    time tar -c ${dest} > /dev/null
done
