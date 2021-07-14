#!/usr/bin/env bash

set -o pipefail

DD_SIZE="2G"

human_to_k() {
	initial="${1,,}"
	value=${initial:0:$((${#initial} - 1))}
	suffix=${initial: -1}

	case "${suffix}" in
		k) echo "${value}";;
		m) echo "$((${value} * 1024))";;
		g) echo "$((${value} * 1048576))";;
		t) echo "$((${value} * 1073741824))";;
	esac
}

for device in "$@"; do
        echo "Device: ${device}"
        for block_size in 4k 8k 16k 32k 64k 128k 256k 512k 1M; do
		block_count=$(($(human_to_k "${DD_SIZE}") / $(human_to_k "${block_size}")))
                echo -n "  * Testing ${block_count} x ${block_size}: "
		if results=($(dd if=${device} of=/dev/null iflag=direct,sync bs=${block_size} count=${block_count} 2>&1 | grep "copied" | awk '{ print $1, $10, $11 }')); then
			echo "${results[1]} @ ${results[2]} ${results[3]}"
		else
			echo "DD exection failed."
		fi
		# dd_status=$?
		# echo "Status: ${dd_status}"
		# echo -e "      Bytes: ${results[1]}\n      Speed: ${results[2]} ${results[3]}"
        done
        echo ""
done

