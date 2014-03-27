#!/bin/bash

LOOPCOUNT=3
TESTOPTS="-ceI "
BLOCKSIZES="4 8 16 32 64 128 256"
TESTLIST="-i 1 -i 2 -i 3 -i 4 -i 5 -i 6 -i 7 -i 8 -i 9 -i 10 -i 11 -i 12"

memsize="$(grep MemTotal /proc/meminfo | awk '{ print $2 }')"
filesize="$(($memsize * 2))"
testpath="$1"
logpath="$2"

showusage() {
	scriptname="$(basename $0)"
	echo ""
	echo "${scriptname} - IOZone wrapper script"
	echo ""
	echo "Usage:"
	echo "------"
	echo "${scriptname} testpath logpath"
	echo ""
	echo " testpath - Path to perform iozone tests in"
	echo " logpath  - Path to output iozone logs to"
	echo ""
}

if [ "$testpath" == "" ]; then
	echo ""
	echo "ERROR: You must supply a path for test file(s)!"
	showusage
	exit 1
fi

if [ "$logpath" == "" ]; then
	echo ""
	echo "ERROR: You must supply a path for test logs!"
	showusage
	exit 1
fi


for c in $(seq 0 $LOOPCOUNT); do
	for r in $BLOCKSIZES; do
		params=" ${TESTLIST} ${TESTOPTS} -s ${filesize} -r ${r} -f ${testpath}/iozone-r${r}-${c}.data"

		echo "Test ${c} / Block size: ${r}"
		iozone $params | tee ${logpath}/iozone-r${r}-${c}.log
	done
done
