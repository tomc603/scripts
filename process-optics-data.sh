#!/usr/bin/env bash

for logfile in ~/Google\ Drive/My\ Drive/Documents/Switch\ Optics\ Data/*.log; do
    echo "${logfile}"
    csvfile="${logfile%.log}.csv"
    grep -E "^Et.*$" "${logfile}" | awk '{OFS=","}; { print "\x22"$1"\x22",$2,$3,$4,$5,$6,$7 }' > "${csvfile}"
done

for csvfile in ~/Google\ Drive/My\ Drive/Documents/Switch\ Optics\ Data/*.csv; do
    echo "${csvfile}"
    switchfile="$(basename "${csvfile}")"
    switchname="${switchfile%.csv}"
    awk '{ OFS=","; NAME="'$switchname'" }; { print NAME,$1 }' "${csvfile}" >> ~/Google\ Drive/My\ Drive/Documents/Switch\ Optics\ Data/portdata.csv
done
