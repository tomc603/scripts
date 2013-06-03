#!/usr/bin/env python

#
# This script searches through DNS query log files for the specified zone name.
# The search is performed for a specified date entered on the comand line.
#
# TODO:
# Write to log file with multiple threads if needed
#

import csv
import bz2
import datetime
import glob
from cStringIO import StringIO
import logging
import hashlib
import multiprocessing
import optparse
import os
import sys
import time
# import fnmatch

class statistics():
    """
        This class contains all of the statistical functions.
        i.e.: topnames, topsources, topqtypes, etc.
    """

    def topnames(self, count):
        """
            This function returns the top 'count' queried names

            @param count: The number of results to return
            @type count: int

            @return: Dictionary of queried names and query count
            @rtype: dict
        """
        return None

    def topsources(self, count):
        """
            This function returns the top 'count' query source IP addresses

            @param count: The number of results to return
            @type count: int

            @return: Dictionary of top source IP addresses and query count
            @rtype: dict
        """
        return None

    def topquerytypes(self, count):
        """
            This function returns the top 'count' query types

            @param count: The number of results to return
            @type count: int

            @return: Dictionary of top query types and query count
            @rtype: dict
        """
        return None


def filecollector(q, o, searchzone):
    """
        For the directory passed, find all files in the glob beneath it and
        add it to the queue 'q'.
        If e.isSet() is True, we need to exit the thread.
    """
    scriptlogger.debug('filecollector doesn\'t do anything yet.')


def findlines(lines, domlist, anonymize, namedict, hashdict):
    """
        Generator to return lines matching a domain in the list 'domlist'
    """
    # List of the domains we want to search for, preceeded with a '.'
    dotdomlist = ['.' + x for x in domlist]

    for line in lines:
        # Split the line on '.', and keep the right-most two groups
        # [domain, tld]. Join these two fields with a '.', and test if the
        # result is in the list of domains we want.

        # Convert the log line's queried name to lowercase. Saves dictionary
        # entries for mixed-case queries and matches lower-case search list
        # entries properly.
        searchdom = line[8].lower()
        if searchdom in namedict:
            if namedict[searchdom] is True:
                scriptlogger.debug('Server name is a previous match.')
                if anonymize:
                    # Override the server's name to anonymize our network.
                    # The full server name should be in field #3
                    servername = line[3]
                    # Retrieve the site name (ie. ewr, ams...)
                    sitename = ''.join(servername.split('-')[-1:])
                    if not servername in hashdict:
                        # Instead of calculating the same MD5 for
                        # every line with the same server name,
                        # build a dictionary with the hash values
                        # and save lots of CPU time.
                        scriptlogger.debug('Server\'s hash not found'
                                        ' in dictionary. Adding.')
                        hashdict[servername] = \
                            hashlib.md5(servername).hexdigest()
                    # Combine the MD5 and the site name for the new
                    # server name in the output file
                    line[3] = hashdict[servername] + '-' + sitename
                yield ' '.join(line) + '\n'
        elif searchdom.endswith(tuple(dotdomlist)) or searchdom in domlist:
            # The queried name is in the list of domains we're searching for
            # or it ends with one of the domains preceeded with a '.'
            scriptlogger.debug('Matching line found. Adding entry to name'
                            ' dictionary.')
            namedict[searchdom] = True
            if anonymize:
                scriptlogger.debug('Anonymizing output.')
                # Override the server's name to anonymize our network.
                # The full server name should be in field #3
                servername = line[3]
                # Retrieve the site name (ie. ewr, ams...)
                sitename = ''.join(servername.split('-')[-1:])
                if not servername in hashdict:
                    # Instead of calculating the same MD5 for
                    # every line with the same server name,
                    # build a dictionary with the hash values
                    # and save lots of CPU time.
                    scriptlogger.debug('Server\'s hash not found'
                                    ' in dictionary. Adding.')
                    hashdict[servername] = \
                        hashlib.md5(servername).hexdigest()
                # Combine the MD5 and the site name for the new
                # server name in the output file
                line[3] = hashdict[servername] + '-' + sitename
            yield ' '.join(line) + '\n'
        else:
            # This outputs an astounding about of useless data.
            # scriptlogger.debug('Marking non-matching entry in dictionary.')
            namedict[searchdom] = False


def dequeue(q, o, searchzones, compress):
    """
        Process each file in the queue 'q', searchinf for the zone 'searchzone'.
        If e.isSet() is True, we need to exit the thread.
    """
    # Create a dictionary that lives as long as this process to contain
    # queried names and their desirability.
    procnamedict = {}

    # Create a dictionary that lives as long as this process to contain
    # hashed server names.
    hashdict = {}

    while not q.empty():
        try:
            # StringIO() functions are extremely fast, which reduces the time
            # required to append log lines to our output collector.
            outputlines = StringIO()
            # Fetch an item from the queue, and do not wait for an item to be
            # available. If one isn't available, we catch the exception below.
            processitem = q.get(False)
            scriptlogger.debug('Dequeued file %s', processitem)
            scriptlogger.error('[ %1.1f%% ]', float(filequeue.qsize()) /
                float(MAXQUEUEDEPTH) * 100)

            # Test the extension and process accordingly
            if processitem.endswith('.bz2'):
                # The file found ends in .bz2. Use the python bzip2 handling
                # module to decompress and read the file into the variable 'f'.
                scriptlogger.debug('Reading compressed input file.')
                csvfile = csv.reader(bz2.BZ2File(processitem, 'rb'),
                    delimiter = ' ', skipinitialspace = True)
            else:
                # The file is assumed to be uncompressed text. This may be wrong,
                # but importing unneeded libraries like gzip is probably more
                # wrong.
                scriptlogger.debug('Reading uncompressed input file.')
                csvfile = csv.reader(open(processitem, 'r'), delimiter = ' ',
                    skipinitialspace = True)
            scriptlogger.debug('Finished reading input file.')

            # Use a generator to produce the output lines we want.
            #
            # NOTE: Generators are way faster than normal for loops somehow,
            # even though the generator is basically a for loop wrapped in a
            # function.
            scriptlogger.debug('Creating search generator')
            matchlines = findlines(csvfile, searchzones, options.anonymize,
                procnamedict, hashdict)
            scriptlogger.debug('Finished creating search generator')

            # Append the query log lines to the output variable
            scriptlogger.debug('Copying matching lines from generator')
            for line in matchlines:
                outputlines.write(line)
            scriptlogger.debug('Finished copying matching lines from generator')

            # Put our output data on a queue for the writer process to pick up.
            if compress is True:
                # We need to compress our output before putting it on the queue
                scriptlogger.debug('Adding compressed output lines to queue')
                o.put(bz2.compress(outputlines.getvalue()))
            else:
                # We are writing a raw text output. Don't compress the output.
                scriptlogger.debug('Adding output lines to queue')
                o.put(outputlines.getvalue())
            scriptlogger.debug('Finished adding output lines to queue')

        except multiprocessing.queues.Empty:
            # There are no more file items on the queue to process, but the
            # thread has been spawned anyway. This is common, so handle it
            # gracefully.
            scriptlogger.debug('File queue is empty')
        except KeyboardInterrupt:
            # The current process has caught CTRL+C. Raise an exit value so
            # python understands what happened.
            scriptlogger.debug('CTRL-C received. Raising SystemExit.')
            raise SystemExit(255)

        # Print some stats about dictionaries.
        scriptlogger.debug('Hash dict items: %0.0f', len(hashdict))
        scriptlogger.debug('Name dict items: %0.0f', len(procnamedict))


def writer(q, outfile):
    """
        Write data from queue 'q' to the file 'outfile'. If 'compress' is True
        then we need to compress the data as we write it.
    """
    try:
        if outfile is None:
            # We are logging plain text. Specify a buffer size to reduce
            # IO operations on disk hardware.
            scriptlogger.debug('Writing query log output to STDOUT')
            queryoutput = sys.stdout
        else:
            scriptlogger.debug('Writing query log output file')
            queryoutput = open(outfile, mode = 'wb', buffering = BUFFSIZ)
    except:
        # The user has specified an output file, and we can't open it for
        # writing. Alert them and write to STDOUT to be safe.
        scriptlogger.critical('Could not open output file for write! ' +
            'Writing output to STDOUT.')
        queryoutput = sys.stdout

    while True:
        # Fetch items from the output queue and write them to the output
        # file. These items should already be compressed by their worker
        # process if needed.
        try:
            queryoutput.write(q.get(timeout = 10))
            scriptlogger.debug('Data found on the output queue.')
        except multiprocessing.queues.Empty:
            scriptlogger.debug('Output queue is empty.')
            continue
        except:
            scriptlogger.debug('Exception caught while processing output queue.')
            break
        queryoutput.flush()

    scriptlogger.debug('Flushing output files')
    queryoutput.flush()
    queryoutput.close()
    scriptlogger.debug('Finished flushing output files')


#
# Run the meat of the script
#
if __name__ == '__main__':
    #
    # Set up script defaults
    #

    # Version of the script, included in the help output.
    SCRIPTVER = '1.1'

    # bz2 output file buffer size
    BUFFSIZ = 65536
    # bz2 output file compression level
    COMPLVL = 9
    # Default logging level for script logging
    LOGLEVEL = logging.CRITICAL
    # Calculate yesterday's date for default date globs
    YESTERDAY = datetime.date.today() - datetime.timedelta(days = 1)

    # Default value to increment the range() function for start and end values.
    DEFAULTINCREMENT = 300

    # Figure out the number of processors, and use that later
    # to start up CPUCOUNT threads by default
    CPUCOUNT = multiprocessing.cpu_count() - 1

    # Default file queue size.
    MAXQUEUEDEPTH = 0

    # Set up the output Queue
    outputqueue = multiprocessing.Queue()

    # Set up a queue to hold commands to be sent to child processes.
    # At this time, we only use this to signal the writer process to stop.
    #
    # TODO: This should really be converted into a Pipe() between the main
    # process and each of the child processes we spawn.
    commandqueue = multiprocessing.Queue()

    # Create a logger for script output
    scriptlogger = logging.getLogger('dailyzonequeries')
    # Set the default logging level for the script's logger
    scriptlogger.setLevel(LOGLEVEL)
    # Create a stream handler to control logging output
    loghandler = logging.StreamHandler(sys.stderr)
    # Set an output format for script log lines. We include the time,
    # process name, and the message sent to the log.
    logformatter = logging.Formatter('%(asctime)s - %(processName)s - '
        '%(message)s')
    # Add the log format to the log handler
    loghandler.setFormatter(logformatter)
    # Add the log handler to the script's logger
    scriptlogger.addHandler(loghandler)
    scriptlogger.debug('Script logging enabled')

    # Handle the command line options, configure logging if specified
    scriptlogger.debug('Processing CLI options')
    # Create the option parser, and give a small usage example.
    optionparser = optparse.OptionParser(usage = '%prog [options] -b '
        '/some/log/dir -z example.com', version = SCRIPTVER)

    # Specify the valid options available in the script, and the variables
    # to store their arguments in. Also provide a helpful description for each
    # option to be output when a user specifies '--help'.
    optionparser.add_option('-a', '--anon', default = False, dest = 'anonymize',
        action = 'store_true', help = 'Anonymize internal host data. '
        'Default: False.')
    optionparser.add_option('-b', '--basedir', default = '.', dest = 'basedir',
        help = 'Base directory to perform query log search in. '
        'Default: Current directory.')
    optionparser.add_option('-c', '--compress', default = False,
        dest = 'compressquerylog', action = 'store_true',
        help = 'Compress the output query log file. Automatically adds .bz2 '
        'extension. '
        'Default: False.')
    optionparser.add_option('-d', '--day', default = str(YESTERDAY.day),
        dest = 'queryday', help = 'Day to perform query log search on. '
        'Default: Yesterday')
    optionparser.add_option('-e', '--end', default = None, dest = 'epochend',
        type = int, help = 'Epoch timestamp of the last log file. '
        'Default: None')
    optionparser.add_option('-f', '--file', default = '*', dest = 'queryfilefilter',
        help = 'Filter to narrow query files down. '
        'Default: *')
    optionparser.add_option('-i', '--increment', default = None, dest = 'epochinc',
        type = int, help = 'Number to increment timestamp by. '
        'Default: None')
    optionparser.add_option('-l', '--log', default = None, dest = 'scriptlogfile',
        help = 'Log file for script messages. '
        'Default: STDERR')
    optionparser.add_option('-m', '--month', default = str(YESTERDAY.month),
        dest = 'querymonth',
        help = 'Month to perform query log search on. '
        'Default: Yesterday')
    optionparser.add_option('-o', '--output', default = None,
        dest = 'queryoutputfile',
        help = 'Log file for query entries found. '
        'Default: zone.YYYY-MM-DD.log')
    optionparser.add_option('-s', '--start', default = None, dest = 'epochstart',
        type = int, help = 'Epoch timestamp of the first log file. '
        'Default: None')
    optionparser.add_option('-t', '--threads', default = CPUCOUNT,
        dest = 'scriptthreads', type = int,
        help = 'Threads to use for query log processing. '
        'Default: CPU count')
    optionparser.add_option('-v', '--verbose', default = 0, dest = 'scriptverbose',
        action = 'count', help = 'Increase verbosity this script should have 0-5. '
        'Default: 0')
    optionparser.add_option('-y', '--year', default = str(YESTERDAY.year),
        dest = 'queryyear', help = 'Year to perform query log search on. '
        'Default: Yesterday')
    optionparser.add_option('-z', '--zone', default = None, action = 'append',
        dest = 'queryzones', help = 'Zone name to find in query logs. '
        'Default: None (All)')

    # Parse the options and arguments passed on the command line
    options, args = optionparser.parse_args()

    #
    # Check option sanity and assign values for script parameters
    #
    if options.scriptlogfile:
        # Log script messages to the specified log file.
        # NOTE: We remove the STDERR handler, so logging is done to STDERR
        # OR to the specified file, but not both.
        try:
            # Log diagnostic output to a file instead of STDERR
            logfilehandler = logging.FileHandler(options.scriptlogfile)
            # Add the log format to the log handler
            logfilehandler.setFormatter(logformatter)
            # Add the log handler to the script's logger
            scriptlogger.addHandler(logfilehandler)
            # Remove the STDERR log handler created by default
            scriptlogger.removeHandler(loghandler)
        except:
            scriptlogger.critical('Could not log messages to the specified file!')

    if options.scriptverbose == 0:
        # Default logging level
        scriptlogger.setLevel(logging.CRITICAL)
        scriptlogger.debug('Logging level set to CRITICAL')
    elif options.scriptverbose == 1:
        # Logging level for -v
        scriptlogger.setLevel(logging.ERROR)
        scriptlogger.debug('Logging level set to ERROR')
    elif options.scriptverbose == 2:
        # Logging level for -vv
        scriptlogger.setLevel(logging.WARNING)
        scriptlogger.debug('Logging level set to WARNING')
    elif options.scriptverbose == 3:
        # Logging level for -vvv
        scriptlogger.setLevel(logging.INFO)
        scriptlogger.debug('Logging level set to INFO')
    else:
        # Logging level for -vvvv+
        scriptlogger.setLevel(logging.DEBUG)
        scriptlogger.debug('Logging level set to DEBUG')

    if options.epochstart and not options.epochend:
        scriptlogger.critical('A start timestamp has been specified without'
            ' an end timestamp! Check the --end parameter.')
        sys.exit(1)

    if options.epochend and not options.epochstart:
        scriptlogger.critical('An end timestamp has been specified without'
        ' a start timestamp! Check the --start parameter.')
        sys.exit(1)

    if options.epochinc and (not options.epochstart or not options.epochstart):
        scriptlogger.critical('A timestamp increment has been specified without'
        ' a start or end timestamp! Check the --start or --end parameter.')
        sys.exit(1)

    if not glob.glob(options.basedir):
        # The glob of basedir isn't returning anything! Bail out to be safe.
        scriptlogger.critical('Please check the basedir parameter! ' +
            'No subdirectories returned!')
        sys.exit(1)

    if not glob.glob(os.path.join(options.basedir, options.queryyear)):
        # The glob of basedir and year isn't returning anything!
        # Bail out to be safe.
        scriptlogger.critical('Please check the year parameter! ' +
            'No subdirectories returned!')
        sys.exit(1)

    if not glob.glob(os.path.join(options.basedir, options.queryyear,
        options.querymonth)):
        # The glob of basedir, year, and month isn't returning anything!
        # Bail out to be safe.
        scriptlogger.critical('Please check the month parameter! ' +
            'No subdirectories returned!')
        sys.exit(1)

    if not glob.glob(os.path.join(options.basedir, options.queryyear,
        options.querymonth, options.queryday)):
        # The glob of basedir, year, month, and day isn't returning anything!
        # Bail out to be safe.
        scriptlogger.critical('Please check the day parameter! ' +
            'No subdirectories returned!')
        sys.exit(1)

    if options.scriptthreads <= 0:
        # The user tried to specify '0' threads. Force a minimum of 1.
        scriptlogger.error('Incorrect threads parameter passed. ' +
        'Defaulting to 1')
        options.scriptthreads = 1

    if not options.queryzones:
        # No zone was specified, so we have nothing to search for!
        # Inform the user and bail out to be safe.
        scriptlogger.critical('You must specify at least one zone!')
        sys.exit(1)
    else:
        queryzonelist = [q.lower() for q in options.queryzones]

    if options.compressquerylog:
        if not options.queryoutputfile:
            scriptlogger.critical('You can not compress output to STDOUT!')
            sys.exit(1)
        elif not options.queryoutputfile.endswith('.bz2'):
            options.queryoutputfile = options.queryoutputfile + '.bz2'

    # Set up the start and end range list if a range has been specified.
    namerangelist = None
    if options.epochstart and options.epochend:
        if options.epochinc:
            namerangelist = range(options.epochstart, options.epochend + 1,
                options.epochinc)
        else:
            namerangelist = range(options.epochstart, options.epochend + 1,
                DEFAULTINCREMENT)

    # Set up the file Queue.
    scriptlogger.debug('Creating query log file queue')
    filequeue = multiprocessing.Queue()

    # Process each directory found by glob.glob
    # This could be sped up by making a threaded file searcher- one thread per
    # directory returned by glob.glob(). For now, it's fast enough using
    # the walk() function.
    try:
        for globdir in glob.glob(os.path.join(options.basedir,
            options.queryyear, options.querymonth,
            options.queryday)):
            for (dirpath, dirnames, filenames) in os.walk(globdir):
                for datafile in filenames:
                    if namerangelist:
                        try:
                            if int(datafile.split('.')[0]) in namerangelist:
                                filequeue.put(os.path.join(dirpath, datafile))
                                scriptlogger.debug('[%d] Queueing file %s',
                                    filequeue.qsize(), os.path.join(dirpath, datafile))
                        except:
                            continue
                    else:
                        filequeue.put(os.path.join(dirpath, datafile))
                        scriptlogger.debug('[%d] Queueing file %s',
                            filequeue.qsize(), os.path.join(dirpath, datafile))
    except:
        scriptlogger.error('Error globbing %s', os.path.join(options.basedir,
            options.queryyear, options.querymonth,
            options.queryday))

    # Collect the total size of the file queue for status messages later
    MAXQUEUEDEPTH = filequeue.qsize()
    scriptlogger.info('Items queued: %d', MAXQUEUEDEPTH)

    # Set up the worker threads. One per CPU, or the number specified on the
    # command line.
    scriptlogger.debug('Spawning worker processes')
    for i in xrange(options.scriptthreads):
        # Create a thread, point it at our dequeue function, and pass it
        # the queue of file items, the output file handle, the zone to search
        # for, and the event to watch to enable quitting upon user request.
        t = multiprocessing.Process(target = dequeue, args = (filequeue,
            outputqueue, queryzonelist, options.compressquerylog,),
            name = 'LogProcessor-' + str(i))

        # Daemonizing threads means the main program won't leave threads
        # running and quit.
        t.daemon = True

        # Calling start() makes the threads begin working as we create them.
        t.start()
    scriptlogger.debug('Done spawning worker processes')

    scriptlogger.debug('Spawning writer process')
    wp = multiprocessing.Process(target = writer, args = (outputqueue,
        options.queryoutputfile))
    wp.daemon = True
    wp.start()
    scriptlogger.debug('Done spawning writer process')

    # Wait for the threads to finish working...
    while len(multiprocessing.active_children()) > 2:
        # If the queue is empty, the threads will quit on their own. So we only
        # care how many threads are still running. This prevents us from
        # beginning the cleanup & close processes while threads may still have
        # data to write.
        try:
            # While there are items in the queue and active threads, wait 1 sec.
            scriptlogger.debug('Child processes: %0.0f',
                len(multiprocessing.active_children()))
            time.sleep(1)
        except KeyboardInterrupt:
            # There are items in the queue and threads running, but we've received
            # CTRL-C to quit the script.
            scriptlogger.critical('Caught ctrl-c. Stopping worker threads.')

            while len(multiprocessing.active_children()) > 2:
                # There are still threads running. Print a status message
                # and wait 1 sec for them to complete.
                # If there is a "hung" thread, this could easily loop forever
                # so there should probably be a final timeout.
                scriptlogger.info('Waiting for remaining threads to die... ' +
                str(len(multiprocessing.active_children())))
                time.sleep(1)

            # Exit the while loop. We don't care there's remaining work
            break

    # Finish writing the contents of the output queue, then shut down the
    # writer process. We're done writing data.
    while outputqueue.qsize() > 0:
        scriptlogger.debug('Waiting for write queue to empty...')
        time.sleep(1)

    scriptlogger.debug('Sending stop command to writer process')
    wp.terminate()

    scriptlogger.debug('Finished processing query log queue')
