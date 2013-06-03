#!/usr/local/bin/bash

INPATH="$1"
OUTFILE="$2"

if [ "$OUTFILE" != "" ]; then
	for t in 1340636400 1340636700 1340637000 1340637300 1340637600 1340637900 1340638200 1340638500 1340638800 1340639100 1340639400 1340639700 1340640000; do
		if [ -f $INPATH/$t.bz2 ]; then
			bzgrep "prod.fastly.net " $INPATH/$t.bz2 >> $OUTFILE-$t.log
		else
			echo "$INPATH/$t.bz2 does not exist!"
		fi
	done
else
	echo "No output file specified!"
fi

