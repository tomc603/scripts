#!/usr/bin/env bash

############################################
# File Name: archivequeries.sh
# Date Created: 
# Creator: tcameron
# Last Edited On: 2013-01-05 13:08:38
# Last Edited By: tcameron
#
# Input:
#   Command line arguments:
#     -a ARCHDIR   - Directory containing archived query logs, relative to BASEDIR.
#     -b BASEDIR   - Directory containing original and archive directories
#     -d           - Print verbose debugging messages
#     -n QUERYNAME - Space separated list of names to archive stats for
#     -s SITES     - Space separated list of sites to archive query logs for
#     -t DAYS      - Day in history to archive data for. ie: 89 will archive data
#                    for the day that was today minus 89 days.
#
# Returns:
#   0 - Success
#   1 - Parameter error
#   2 - File access error
#
# Description:
#   This script archives query log entries from $RUNDATE from the specified
#   site(s) for the specified query names. This is done by looping through each
#   host from each site, then looping through the files located in the log
#   directory with the proper date string in its name.
#
#   When a file is found, we use a regex in an awk command to select the lines
#   we need, and then pass those lines to bzip to be placed in the specified
#   archive directory.
#
#   The archive directory has the same structure as the original location of the
#   query log files.
#
#   More information: https://wiki.corp.dyndns.com/x/DZh0AQ
############################################


#------------------------------------------------------------------------------
# Default global variables
#------------------------------------------------------------------------------
DEBUG=0
LOOPERROR=0
DAYCONST=86400
ARCHIVEDAYS=89
EPOCHDATE=`date +%s`
RUNDATE=`date -r $(($EPOCHDATE-($DAYCONST*$ARCHIVEDAYS))) +%Y/%-m/%-d`


#------------------------------------------------------------------------------
# Command line variables
# Set default values for variables set on the CLI
#------------------------------------------------------------------------------
BASEDIR="/logs/logstore/dynect-stats"
ARCHIVEDIR="archive"
SITES=""
QUERYNAME=""


#------------------------------------------------------------------------------
# Helper functions
#------------------------------------------------------------------------------
function printdebug() {
    # If debugging is enabled, print the supplied message
    if [ $DEBUG -ne 0 ]; then
        echo "DEBUG: $*"
    fi
}

function printerror() {
    # Print the supplied message to STDERR
    echo "ERROR: $*" 1>&2
}

function printhelp() {
    # Print script help text.
    echo ""
    echo "`basename $0` -a ARCHDIR -b BASEDIR -d -n QUERYNAME -s SITES"
    echo ""
    echo "  -a ARCHDIR   - Directory containing archived query logs, relative to BASEDIR."
    echo "                 Default: archive/"
    echo "  -b BASEDIR   - Directory containing original and archive directories"
    echo "                 Default: /logs/logstore/dynect-stats"
    echo "  -d           - Print verbose status messages"
    echo "  -h           - Print this help message"
    echo "  -n QUERYNAME - Space seperated list of names to archive stats for"
    echo "                 Default: None (all)"
    echo "  -s SITES     - Space seperated List of sites to archive query logs for"
    echo "                 Default: None"
    echo "  -t DAYS      - Day in the past to archive query logs for"
    echo "                 Default: 89"
    echo ""
}


#------------------------------------------------------------------------------
# CLI option parsing
#------------------------------------------------------------------------------
while getopts "a:b:dhn:s:t:" opt; do
    case $opt in
        a) ARCHIVEDIR=$OPTARG; printdebug "Archive directory: $ARCHIVEDIR" ;;
        b) BASEDIR=$OPTARG ; printdebug "Base directory   : $BASEDIR" ;;
        d) DEBUG=1 ; printdebug "Debugging        : Enabled" ;;
        h) printhelp; exit 0 ;;
        n) QUERYNAME=$OPTARG ; printdebug "Query names      : $QUERYNAME" ;;
        s) SITES=$OPTARG; printdebug "Sites            : $SITES" ;;
        t) ARCHIVEDAYS=$OPTARG; printdebug "Archive days     : $ARCHIVEDAYS" ;;
        *) printhelp; exit 1 ;;
    esac
done


#------------------------------------------------------------------------------
# CLI option checking
#------------------------------------------------------------------------------
printdebug "Checking command line options"
if [ "$BASEDIR" == "" ]; then
    # BASEDIR not provided
    printerror "You MUST provide a base directory."
    exit 1
fi

if [ ! -d $BASEDIR ]; then
    # BASEDIR does not exist
    printerror "Base directory does not exist."
    exit 2
fi

if [ "$ARCHIVEDIR" == "" ]; then
    # ARCHIVEDIR not provided
    printerror "You MUST provide an archive directory."
    exit 1
fi

if [ ! -d $BASEDIR/$ARCHIVEDIR ]; then
    # Directory $BASEDIR/$ARCHIVEDIR does not exist
    printerror "Archive directory does not exist."
    exit 2
fi

if [ "$ARCHIVEDAYS" == "" ]; then
    # Blank archive days was specified
    printerror "You MUST specify a number of archive days."
    exit 1
elif [ $ARCHIVEDAYS -gt 0 ]; then
    RUNDATE=`date -r $(($EPOCHDATE-($DAYCONST*$ARCHIVEDAYS))) +%Y/%-m/%-d`
    printdebug "Query log date: $RUNDATE"
else
    # Zero or negative archive days was specified
    printerror "You MUST specify a number of archive days greater than zero."
    exit 1
fi

if [ ! "$SITES" ]; then
    # No site(s) were supplied
    printerror "You MUST provide at least one site to archive query logs."
    exit 1
fi

if [ "$QUERYNAME" == "" ]; then
    # No QUERYNAME was supplied
    printdebug "No query name was provided. Defaulting to all."
    querystr="*"
else
    querystr=${QUERYNAME/ /\|}
fi


#------------------------------------------------------------------------------
# Process the query log files and archive their contents
#------------------------------------------------------------------------------
# Enter the base directory
printdebug "Entering $BASEDIR"
pushd $BASEDIR > /dev/null
if [ $? -ne 0 ]; then
    # Confirm we entered the directory
    printerror "Could not enter $BASEDIR"
    exit 2
else
    printdebug "Ok"
fi

# Loop through each specified site
printdebug "Starting site loop"
for cursite in $SITES; do
    printdebug "Processing site: $cursite"

    # Loop through each dns4 host's directory for each site
    for hostdir in dns4-*-$cursite.dyndns.com; do
        printdebug "Processing host: $hostdir"

        # Helper variable for keeping track of the directory a log file is in
        logdir=$hostdir/$RUNDATE

        # Archive directory name
        archdir=$BASEDIR/$ARCHIVEDIR/$logdir

        # Confirm the archive directory exists. If not, create it.
        printdebug "Confirming archive directory exists"
        if [ ! -d $archdir ]; then
            printdebug "Archive directory does not exist. Attempting to create."
            mkdir -p $archdir
            if [ $? -ne 0 ]; then
                printerror "Could not create archive directory!"
                exit 2
            else
                printdebug "Ok"
            fi
        else
            printdebug "Ok"
        fi

        # Tell the user what directories we are using
        printdebug "Log dir    : $logdir"
        printdebug "Archive dir: $archdir"

        # Enter the log directoy
        printdebug "Entering $logdir"
        pushd $logdir > /dev/null
        if [ $? -ne 0 ]; then
            # Confirm we entered the directory
            printerror "Could not enter $logdir"
            exit 2
        else
            printdebug "Ok"
        fi

        # Loop through each log file, searching for queries matching QUERYNAME
        for logfile in *.bz2; do
            printdebug "Source: $BASEDIR/$logdir/$logfile"
            printdebug "Dest  : $archdir/$logfile"

            # Cat the compressed file to our awk statement. Matching lines are
            # output to $archdir/$logfile.
            bzcat $logfile | awk '{ if (tolower($9) ~ /(^|.*\.)('$querystr')/)  print $0 }' | bzip2 -cz > $archdir/$logfile

            # Check the status of our pipeline
            pipelinestatus=("${PIPESTATUS[@]}")
            if [ ${pipelinestatus[0]} -ne 0 ]; then
                # bzcat of input file failed
                printerror "Could not read input file $logfile"
                LOOPERROR=1
            elif [ ${pipelinestatus[1]} -ne 0 ]; then
                # awk command failed
                printerror "Filter failed on $logfile"
                LOOPERROR=1
            elif [ ${pipelinestatus[1]} -ne 0 ]; then
                # bzip to output file command failed
                printerror "Could not create output file $archdir/$logfile"
                LOOPERROR=1
            else
                printdebug "Ok"
            fi
        done
        popd > /dev/null
    done
done
popd > /dev/null

# Return an exit code from the loop so we can report non-fatal errors too.
exit $LOOPERROR

