#!/usr/bin/env awk

# This AWK script fetches syslog lines from Postfix that include "delays" data.
#
# The data is logged in the format delays=a/b/c/d where a-d are floating point
# numbers representing the seconds a message was delayed in four distinct
# functions of Postfix relaying.
#
# The data is retrieved from a log line by doing a substring match, then
# splitting the match into an array on the "/" character.
#
# Once we have our array of data, the script outputs the date string and the
# array fields into a CSV format for later processing with other tools.

BEGIN {
	# Set our field separators for sanity's sake
	IFS=" ";
	OFS=" ";

	# Set up a regex to use to select the data from delays=a/b/c/d
	delayregex="[0-9]*\\.?[0-9]*/[0-9]*\\.?[0-9]*/[0-9]*\\.?[0-9]*/[0-9]*\\.?[0-9]*";

	# Print a header for the CSV output
	printf("date,a,b,c,d\n");
}
{
	# If we have a match to our regex...
	if (match($0, delayregex)) {
		# Select the month, day, time from the syslog fields
		monval=$1;
		dayval=$2;
		timeval=$3;

		# Select the log line substring that matches the regex, and
		# split the a/b/c/d formatted string into distinct values
		split(substr($0,RSTART,RLENGTH),delayarray,"/");
		printf("%s %s %s,%s,%s,%s,%s\n", monval, dayval, timeval,
			delayarray[1], delayarray[2], delayarray[3],
			delayarray[4]);
	}
}
