#!/usr/bin/env awk
BEGIN {
	OFS=" ";
	delayregex="[0-9]*\\.?[0-9]*/[0-9]*\\.?[0-9]*/[0-9]*\\.?[0-9]*/[0-9]*\\.?[0-9]*";
	dateval="";
	delaysval="";
	printf("Date,a,b,c,d\n");
}
{
	if (match($0, delayregex)) {
		monval=$1;
		dayval=$2;
		timeval=$3;
		split(substr($0,RSTART,RLENGTH),delayarray,"/");
		printf("%s %s %s,%s,%s,%s,%s\n", monval, dayval, timeval, delayarray[1], delayarray[2], delayarray[3], delayarray[4]);
	}
}
