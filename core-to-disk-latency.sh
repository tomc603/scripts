#!/usr/bin/env bash

# ioping batch output format:
# requests 0, total_time_us 1, iops 2, throughput_bytes_per_second 3, min 4, avg 5, max 6, mdev 7
echo "\"CPU\",\"PATH\",\"IOPS\",\"MIN\",\"AVG\",\"MAX\",\"MDEV\""
for cpu in {0..63}; do
    for dest in /mnt/testing/*; do
        stats=( $(sudo taskset --cpu-list "${cpu}" ioping -w 10s -i 0 -D -S 1g -B "${dest}") )
        echo "${cpu},${dest},${stats[2]},${stats[4]},${stats[5]},${stats[6]},${stats[7]}"
    done
done
