#!/usr/local/bin/bash

rm /home/tcameron/ipdriftlogs/*.log
for reg in ams lon fra; do
	for serv in 01 02 03 04; do
		echo "dns4-$serv-$reg.dyndns.com"
		for before in 1340644800 1340645100 1340645400 ; do
			bzcat /logs/logstore/dynect-stats/dns4-$serv-$reg.dyndns.com/2012/6/25/$before.bz2 >> /home/tcameron/ipdriftlogs/$reg-before.log
		done

		for during in 1340645700 1340646000 1340646300; do
			bzcat /logs/logstore/dynect-stats/dns4-$serv-$reg.dyndns.com/2012/6/25/$during.bz2 >> /home/tcameron/ipdriftlogs/$reg-during.log
		done

		for after in 1340646600 1340646900 1340647200; do
			bzcat /logs/logstore/dynect-stats/dns4-$serv-$reg.dyndns.com/2012/6/25/$after.bz2 >> /home/tcameron/ipdriftlogs/$reg-after.log
		done
	done

	cat /home/tcameron/ipdriftlogs/$reg-before.log | awk '{ print $7 }' | awk -F '#' '{ print $1 }' | sort -n | uniq -c | sort -rn -k 1 | head -n 100 >> /home/tcameron/ipdriftlogs/$reg-before-topaddresses.log
	cat /home/tcameron/ipdriftlogs/$reg-during.log | awk '{ print $7 }' | awk -F '#' '{ print $1 }' | sort -n | uniq -c | sort -rn -k 1 | head -n 100 >> /home/tcameron/ipdriftlogs/$reg-during-topaddresses.log
	cat /home/tcameron/ipdriftlogs/$reg-after.log | awk '{ print $7 }' | awk -F '#' '{ print $1 }' | sort -n | uniq -c | sort -rn -k 1 | head -n 100 >> /home/tcameron/ipdriftlogs/$reg-after-topaddresses.log
done
