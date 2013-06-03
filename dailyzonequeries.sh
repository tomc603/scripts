#!/usr/local/bin/bash

#
# Script to produce a large query log for a single day for a single domain.
#

TOPDIR="/logs/logstore/dynect-stats"

while getopts "d:m:vy:z:" opt; do
	case $opt in
		d) DAY=$OPTARG ;;
		m) MONTH=$OPTARG ;;
		v) VERBOSE="y" ;;
		y) YEAR=$OPTARG ;;
		z) SEARCHDOMAIN=$OPTARG ;;
		*) echo "Usage $0 [-v] -y YEAR -m MONTH -d DAY -z DOMAIN" ; exit 1 ;;
	esac
done

if [ "$YEAR" = "" ]; then
	echo "You MUST specify a year"
	echo "Usage $0 -y [YEAR] -m [MONTH] -d [DAY] -z [DOMAIN]"
	exit 1
elif [ "$MONTH" = "" ]; then
	echo "You MUST specify a month"
	echo "Usage $0 -y [YEAR] -m [MONTH] -d [DAY] -z [DOMAIN]"
	exit 1
elif [ "$DAY" = "" ]; then
	echo "You MUST specify a day"
	echo "Usage $0 -y [YEAR] -m [MONTH] -d [DAY] -z [DOMAIN]"
	exit 1
elif [ "$SEARCHDOMAIN" = "" ]; then
	echo "You MUST specify a domain"
	echo "Usage $0 -y [YEAR] -m [MONTH] -d [DAY] -z [DOMAIN]"
	exit 1
fi

cd $TOPDIR
for d in dns*.dyndns.com; do
	if [ "$VERBOSE" = "y" ]; then echo -e "\nServer: $d" >&2; fi
	if [ -d $TOPDIR/$d/$YEAR/$MONTH/$DAY ]; then
		cd $TOPDIR/$d/$YEAR/$MONTH/$DAY
		for f in *.bz2; do
			if [ "$VERBOSE" = "y" ]; then echo "  -  File: $f" >&2; fi
			if [ "$VERBOSE" = "y" ]; then echo "  -  $TOPDIR/$d/$YEAR/$MONTH/$DAY/$f" >&2; fi
			bzgrep "$SEARCHDOMAIN " $f
		done
	else
		if [ "$VERBOSE" = "y" ]; then echo -e "Skipping.\n Directory $TOPDIR/$d/$YEAR/$MONTH/$DAY does not exist." >&2; fi
	fi
done
