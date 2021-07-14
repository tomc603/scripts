#!/usr/bin/env bash

COLOR_RED='\033[0;31m'
COLOR_NONE='\033[0m'

DEBUG=${DEBUG=0}
RANGE=10

foo () {
	SLEEPTIME=$(( $RANDOM % RANGE + 1 ))
	echo "Sleeping ${SLEEPTIME}"
	sleep ${SLEEPTIME}
	return ${SLEEPTIME}
}

pids=()

for ((i=0;i<10;i++)); do
	foo &
	curpid=$!
	pids+=(${curpid})
	echo "Started PID: ${curpid}"
done

loopcount=0
while true; do
	for pid in ${pids[@]}; do
		echo "Waiting for ${pid}"
		wait ${pid}
		exitval=$?
		echo "PID ${pid} exited: ${exitval}"
		pids=(${pids[@]/${pid}})
	done

	if [[ ${#pids[@]} -eq 0 ]]; then
		echo "Done"
		break
	fi
	sleep 1
done

