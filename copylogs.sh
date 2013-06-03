#!/usr/local/bin/bash
for i in {1341611700..1341618900..300}; do
	for f in `find dns4-* -name $i.bz2 -print`; do
		SRCDIR=`dirname $f`
		mkdir -p /home/tcameron/logs/$SRCDIR && cp -v $f /home/tcameron/logs/$SRCDIR/
	done
done
