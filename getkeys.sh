#!/bin/bash

for SITE in ewr ord pao ams hkg fra lon mia sea syd waw iad lax dfw mht tyo sin; do
	for NUM in 01 02 03 04; do
		SRV="rdns-$NUM-$SITE.dyndns.com"
		ping -c 1 -t 500 $SRV &> /dev/null
		if [ $? -eq 0 ]; then
			echo "Server: $SRV"
			sudo -u system ssh -i /home/system/.ssh/id_dsa system\@$SRV
		fi
	done
done

