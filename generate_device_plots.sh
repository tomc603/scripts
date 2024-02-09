#!/usr/bin/env bash

set -e

declare -a iops_plots
declare -a mbps_plots

for d in *; do
    for f in ${d}/btt/sys_iops_fp.dat; do
        iops_plots+=("\"${f}\" title \"${d}\" with lines")
    done

    for f in ${d}/btt/sys_mbps_fp.dat; do
        mbps_plots+=("\"${f}\" title \"${d}\" with lines")
    done
done


iops_cmd=$(printf ", %s" "${iops_plots[@]}")
mbps_cmd=$(printf ", %s" "${mbps_plots[@]}")

echo "set key noenhanced"
echo "plot ${iops_cmd:2}"
echo "plot ${mbps_cmd:2}"

