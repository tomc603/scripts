#!/bin/bash
while read host; do
	echo "IPv6 addresses for $host"
	ssh -o StrictHostKeyChecking=no $host 'bash -s' << 'ENDSSH'
	ifconfig -a | grep "inet6" | grep -v -e " fc" -e " fe" -e " ::1 " | sed -e 's/^[[:space:]]*//'
ENDSSH
	echo ""
done < hosts.lst
