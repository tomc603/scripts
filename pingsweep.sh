#!/bin/bash

for i in {129..190}; do
    sudo ping -W 1 -i 0.25 -c 3 -S 204.13.248.131 204.13.248.${i} > /dev/null
    if [ $? -eq 0 ]; then
        echo "204.13.248.${i} - UP"
    else
        echo "204.13.248.${i} - DOWN"
    fi
done
