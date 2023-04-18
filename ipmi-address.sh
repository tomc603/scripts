#!/usr/bin/env bash

HOSTNAME=$1

if [[ -z ${HOSTNAME} ]]; then
    echo "You must specify a hostname."
    exit 1
fi

knife search node name:"${HOSTNAME}" -a ipmi.address 2> /dev/null | grep "ipmi.address" | awk '{ print $2 }'
