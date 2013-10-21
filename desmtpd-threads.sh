#!/usr/bin/env bash
while :; do ps -ylC desmtpd.pl --sort=rss | awk '{if($8 > 0) total += $8; n++} END {print ((total/n)/1024) "M per process [" n " procs] (" total/1024 "M total memory used)"}'; sleep 5; done
