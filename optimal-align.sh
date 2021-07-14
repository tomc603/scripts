#!/usr/bin/env bash

declare block_device="$1"
declare device_name="$(basename ${block_device} 2> /dev/null)"

if [[ ! -b ${block_device} || -z ${device_name} ]]; then
    echo "ERROR: Invalid block device specified" >&2
    exit 1
fi

declare -i optimal_io_size=$(cat /sys/block/${device_name}/queue/optimal_io_size 2> /dev/null)
declare -i minimum_io_size=$(cat /sys/block/${device_name}/queue/minimum_io_size 2> /dev/null)
declare -i alignment_offset=$(cat /sys/block/${device_name}/alignment_offset 2> /dev/null)
declare -i physical_block_size=$(cat /sys/block/${device_name}/queue/physical_block_size 2> /dev/null)

if [[ ${optimal_io_size} -eq 0 ]]; then
    echo "ERROR: Unable to detect device optimal I/O size" >&2
    exit 2
fi

if [[ ${minimum_io_size} -eq 0 ]]; then
    echo "ERROR: Unable to detect device minimum I/O size" >&2
    exit 2
fi

if [[ ${physical_block_size} -eq 0 ]]; then
    echo "ERROR: Unable to detect device physical block size" >&2
    exit 2
fi

echo "Optimal I/O      : ${optimal_io_size}"
echo "Alignment Offset : ${alignment_offset}"
echo "Plysical block   : ${physical_block_size}"
echo "Partition start  : $(((${optimal_io_size} + ${alignment_offset}) / ${physical_block_size}))"

