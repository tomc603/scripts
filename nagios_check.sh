#!/bin/bash

exitmsg=`/home/tcameron/queuegraph.py nagios`
exitval=$?

if [ $exitval -eq 0 ]; then
	echo "OK"
	exit $exitval
elif [ $exitval -eq 1 ]; then
	echo "WARNING"
	exit $exitval
elif [ $exitval -eq 2 ]; then
	echo "CRITICAL"
	exit $exitval
else
	echo $exitmsg
	exit $exitval
fi

