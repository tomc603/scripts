#!/usr/bin/env bash
echo "Syncing server 1"
rsync -avz -e "ssh -C" tcameron@172.16.15.165:/home/tcameron/results/fulltest/ ./fulltest/

echo "Syncing server 2"
rsync -avz -e "ssh -C" tcameron@172.16.15.166:/home/tcameron/results/fulltest/ ./fulltest/

echo "Updating results file"
~/svn/tcameron/Scripts/Python/dnsfloodtocsv.py > fulltest.csv

echo "Updating charts"
~/svn/tcameron/Scripts/Python/dnsfloodreport.py
echo "done"
