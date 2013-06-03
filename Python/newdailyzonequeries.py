#!/usr/bin/env python

#
# This script searches through DNS query log files for the specified zone name.
# The search is performed for a specified date entered on the comand line.
#
# Aug 28 23:50:00 dns4-02-lax named[80821]: client 201.120.11.84#29738: query: \
# ns-921.amazon.com IN A -EDC
#
# TODO Arguments:
#	-l [FILE]| --log [FILE]
#		Description: File to log messages to.
#		Default:     STDERR
#
# TODO Script:
#   Convert to using Pandas
#     adddots = lambda x: '.' + x
#
#     dataheader = ['qmonth', 'qday', 'qtime', 'qhost', 'qdaemon', 'qclimark', \
#       'qcliaddr', 'qaction', 'qname', 'qdir', 'qtype', 'qflags']
#
#     df = pd.read_csv(\
#       bz2.BZ2File('/home/tcameron/tmp/2012/8/28/1346197800.bz2'), \
#       header=False, names=dataheader, sep='\s*')
#
#     criteria = df['qname'].map(lambda x: x.endswith(tuple(map(adddots, \
#       domlist)) or x in tuple(domlist))
#
#     newdata = df[criteria]
#     newdata.to_csv(outfile, header=False, index=False, sep=' ')
#


import bz2
import datetime
import glob
from cStringIO import StringIO
import logging
import md5
import multiprocessing
import optparse
import os
import pandas as pd
import Queue
import sys
import time
#import threading
#import fnmatch


def filecollector(q, o, e):
	"""
		For the directory passed, find all files in the glob beneath it and
		add it to the queue 'q'.
		If e.isSet() is True, we need to exit the thread.
	"""
	scriptlogger.debug('filecollector doesn\'t do anything yet.')


def dequeue(q, o, searchzones):
	"""
		Process each file in the queue 'q', searchinf for the zone 'searchzone'.
		If e.isSet() is True, we need to exit the thread.
	"""
	# Column titles to be assigned to data read from query log files.
	incols = ['qmonth', 'qday', 'qtime', 'qhost', 'qdaemon', 'qclimark', \
		'qcliaddr', 'qaction', 'qname', 'qdir', 'qtype', 'qflags']

	# Define the columns we want in our output.
	outcols = ['qmonth', 'qday', 'qtime', 'qhost', 'qclimark', 'qcliaddr', \
		'qaction', 'qname', 'qdir', 'qtype', 'qflags']

	while not q.empty():
		try:
			# StringIO() functions are extremely fast, which reduces the time
			# required to append log lines to our output collector.
			outputdata = StringIO()
			# Fetch an item from the queue, and do not wait for an item to be
			# available. If one isn't available, we catch the exception below.
			processitem = q.get(False)
			scriptlogger.error('[ %1.1f%% ]', float(q.qsize()) / \
				float(MAXQUEUEDEPTH) * 100)
			scriptlogger.debug('Dequeueing file %s', processitem)

			# Set a sane initial value for the file
			scriptlogger.debug('Building temporary DataFrame')
			df = pd.DataFrame()
			scriptlogger.debug('Done temporary DataFrame')

			# Get the file extension so we know how to read real data from it
			fileext = os.path.splitext(processitem)[1]

			# Test the extension and process accordingly
			scriptlogger.debug('Reading querylog into DataFrame')
			if fileext == ".bz2":
				# The file found ends in .bz2. Use the python bzip2 handling
				# module to decompress and read the file into the variable 'f'.
				df = pd.read_csv(bz2.BZ2File(processitem, \
					'rb'), header=False, names=incols, sep='\s*')
			else:
				# The file is assumed to be uncompressed text. This may be wrong,
				# but importing unneeded libraries like gzip is probably more
				# wrong.
				df = pd.read_csv(processitem, \
					header=False, names=incols, sep='\s*')
			scriptlogger.debug('Finished reading querylog into DataFrame')

			# Specify the DataFrame search criteria
			scriptlogger.debug('Building search criteria')
			criteria = df['qname'].map(lambda x: \
				x.endswith(tuple(map(dotlam, searchzones))) or x in \
				tuple(searchzones))
			scriptlogger.debug('Finished building search criteria')

			# Execte the search, storing the result in a new DataFrame.
			scriptlogger.debug('Searching DataFrame for criteria')
			rdf = df[criteria]
			scriptlogger.debug('Finished searching DataFrame for criteria')

			if options.anonymize:
				scriptlogger.debug('Anonymizing result data')
				# We are replacing server name & number with an MD5 hash
				# but keeping the site name component. This keeps our
				# network anonymous to our customers, while still providing
				# site information and a unique server ID.
				# ie: dns4-01-lax => md5hashval-lax
				for qhost in rdf.qhost.unique():
					rdf.qhost.replace(qhost, hashlam(qhost), inplace=True)
				scriptlogger.debug('Finished anonymizing result data')

			# Convert DataFrame to StringIO buffer so we can optionally
			# compress them, and write them out to the output stream.
			scriptlogger.debug('Converting results to text')
			rdf.to_csv(outputdata, header=False, cols=outcols, index=False, \
				sep=' ')
			scriptlogger.debug('Finished converting results to text')

			# Write the StringIO data to a file object.
			if options.compressquerylog:
				# Compress StringIO data in the thread so we get the benefit
				# of parallel compression.
				scriptlogger.debug('Compressing & writing results')
				o.write(bz2.compress(outputdata.getvalue()))
				scriptlogger.debug('Finished compressing & writing results')
			else:
				# Write the output as raw text.
				scriptlogger.debug('Writing results')
				o.write(outputdata.getvalue())
				scriptlogger.debug('Finished writing results')

			# Remove the processed item from the queue
			scriptlogger.debug('Marking queue item complete and cleaning up.')
			outputdata.close()
			q.task_done()
		except Queue.Empty:
			# There are no more file items on the queue to process, but the
			# thread has been spawned anyway. This is common, so handle it
			# gracefully.
			scriptlogger.debug('File queue is empty')
		except KeyboardInterrupt:
			# The current process has caught CTRL+C. Raise an exit value so
			# python understands what happened.
			raise SystemExit(255)


#
# Run the meat of the script
#
if __name__ == '__main__':
	#
	# Set up script defaults
	#

	# Version of the script, included in the help output.
	SCRIPTVER = '0.1'

	# bz2 output file buffer size
	BUFFSIZ = 65536
	# bz2 output file compression level
	COMPLVL = 9
	# Default logging level for script logging
	LOGLEVEL = logging.CRITICAL
	# Calculate yesterday's date for default date globs
	YESTERDAY = datetime.date.today() - datetime.timedelta(days=1)
	# Default CPU count for subsequent thread count
	CPUCOUNT = 0

	# Default value to increment the range() function for start and end values.
	DEFAULTINCREMENT = 300

	# Figure out the number of processors, and use that later
	# to start up CPUCOUNT threads by default
	ncpus = os.sysconf("SC_NPROCESSORS_ONLN")
	if isinstance(ncpus, int) and ncpus > 0:
		CPUCOUNT = ncpus - 1

	# multiprocessing only exists in Python 2.6+. It was backported to
	# previous versions, but it's best to not rely on that kind of thing
	# for systems of unknown age.
	#CPUCOUNT = multiprocessing.cpu_count()
	MAXQUEUEDEPTH = 0

	# By default, output query log lines to STDOUT
	queryoutput = sys.stdout

	# Lambda function to add a '.' to an item passed to the function.
	dotlam = lambda x: '.' + x

	# Lambda function to return a hashed string with site code from a
	# three-part server name.
	hashlam = lambda x: md5.new(x).hexdigest() + '-' + x.rsplit('-', 1)[1]

	# Create a logger for script output
	scriptlogger = logging.getLogger('dailyzonequeries')
	# Set the default logging level for the script's logger
	scriptlogger.setLevel(LOGLEVEL)
	# Create a stream handler to control logging output
	loghandler = logging.StreamHandler(sys.stderr)
	# Set the default logging level for the log handler
	loghandler.setLevel(LOGLEVEL)
	# Set an output format for script log lines. We include the time,
	# thread name, log level triggered, and the message sent to the log.
	logformatter = logging.Formatter('%(asctime)s - %(threadName)s - ' +
		'%(levelname)s - %(message)s')
	# Add the log format to the log handler
	loghandler.setFormatter(logformatter)
	# Add the log handler to the script's logger
	scriptlogger.addHandler(loghandler)
	scriptlogger.debug('Script logging enabled')

	# Handle the command line options, configure logging if specified
	scriptlogger.debug('Processing CLI options')
	# Create the option parser, and give a small usage example.
	optionparser = optparse.OptionParser(usage='%prog [options] -b '
		'/some/log/dir -z example.com', version=SCRIPTVER)

	# Specify the valid options available in the script, and the variables
	# to store their arguments in. Also provide a helpful description for each
	# option to be output when a user specifies '--help'.
	optionparser.add_option('-a', '--anon', default=False, dest='anonymize',
		action='store_true', help='Anonymize internal host data. '
		'Default: False.')
	optionparser.add_option('-b', '--basedir', default='.', dest='basedir',
		help='Base directory to perform query log search in. '
		'Default: Current directory.')
	optionparser.add_option('-c', '--compress', default=False,
		dest='compressquerylog', action='store_true',
		help='Compress the output query log file. Automatically adds .bz2 '
		'extension. '
		'Default: False.')
	optionparser.add_option('-d', '--day', default=str(YESTERDAY.day),
		dest='queryday', help='Day to perform query log search on. '
		'Default: Yesterday')
	optionparser.add_option('-e', '--end', default=None, dest='epochend',
		type=int, help='Epoch timestamp of the last log file. '
		'Default: None')
	optionparser.add_option('-f', '--file', default='*', dest='queryfilefilter',
		help='Filter to narrow query files down. '
		'Default: *')
	optionparser.add_option('-i', '--increment', default=None, dest='epochinc',
		type=int, help='Number to increment timestamp by. '
		'Default: None')
	optionparser.add_option('-l', '--log', default=None, dest='scriptlogfile',
		help='Log file for script messages. '
		'Default: STDERR')
	optionparser.add_option('-m', '--month', default=str(YESTERDAY.month),
		dest='querymonth',
		help='Month to perform query log search on. '
		'Default: Yesterday')
	optionparser.add_option('-o', '--output', default=None,
		dest='queryoutputfile',
		help='Log file for query entries found. '
		'Default: zone.YYYY-MM-DD.log')
	optionparser.add_option('-s', '--start', default=None, dest='epochstart',
		type=int, help='Epoch timestamp of the first log file. '
		'Default: None')
	optionparser.add_option('-t', '--threads', default=CPUCOUNT,
		dest='scriptthreads', type=int,
		help='Threads to use for query log processing. '
		'Default: CPU count')
	optionparser.add_option('-v', '--verbose', default=0, dest='scriptverbose',
		action='count', help='Increase verbosity this script should have 0-5. '
		'Default: 0')
	optionparser.add_option('-y', '--year', default=str(YESTERDAY.year),
		dest='queryyear', help='Year to perform query log search on. '
		'Default: Yesterday')
	optionparser.add_option('-z', '--zone', default=None, action='append',
		dest='queryzones', help='Zone name to find in query logs. '
		'Default: None (All)')

	# Parse the options and arguments passed on the command line
	options, args = optionparser.parse_args()

	# Output some parameter values for verification when debugging
	scriptlogger.debug('Finished processing CLI options')
	scriptlogger.debug('Verbose level: %s', options.scriptverbose)
	scriptlogger.debug('Base dir: %s', options.basedir)
	scriptlogger.debug('Zone: %s', str(options.queryzones))
	scriptlogger.debug('Script log: %s', options.scriptlogfile)
	scriptlogger.debug('Script output: %s', options.queryoutputfile)
	scriptlogger.debug('Thread count: %d', options.scriptthreads)
	scriptlogger.debug('Day: %s', options.queryday)
	scriptlogger.debug('Month: %s', options.querymonth)
	scriptlogger.debug('Year: %s', options.queryyear)

	#
	# Check option sanity and assign values for script parameters
	#
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
		scriptlogger.critical('Incorrect threads parameter passed. ' +
		'Defaulting to 1')
		options.scriptthreads = 1

	if not options.queryzones:
		# No zone was specified, so we have nothing to search for!
		# Inform the user and bail out to be safe.
		scriptlogger.critical('You must specify at least one zone!')
		sys.exit(1)

	if options.queryoutputfile:
		# An output file for query logs has been specified
		try:
			if options.compressquerylog:
				# We are logging compressed data. Add the extension, specify a
				# buffer size to reduce IO operations on disk hardware.
				scriptlogger.debug('Compressing query log output file')
				queryoutput = open(options.queryoutputfile + '.bz2',
					mode='w', buffering=BUFFSIZ)
			else:
				# We are logging plain text. Specify a buffer size to reduce
				# IO operations on disk hardware.
				queryoutput = open(options.queryoutputfile, mode='w',
					buffering=BUFFSIZ)
		except:
			# The user has specified an output file, and we can't open it for
			# writing. Alert them and bail out to be safe.
			scriptlogger.critical('Could not open output file for write! ' +
				'Quitting.')
			sys.exit(1)

	if options.scriptverbose == 0:
		# Default logging level
		loghandler.setLevel(logging.CRITICAL)
		scriptlogger.setLevel(logging.CRITICAL)
		scriptlogger.debug('Logging level set to CRITICAL')
	elif options.scriptverbose == 1:
		# Logging level for -v
		loghandler.setLevel(logging.ERROR)
		scriptlogger.setLevel(logging.ERROR)
		scriptlogger.debug('Logging level set to ERROR')
	elif options.scriptverbose == 2:
		# Logging level for -vv
		loghandler.setLevel(logging.WARNING)
		scriptlogger.setLevel(logging.WARNING)
		scriptlogger.debug('Logging level set to WARNING')
	elif options.scriptverbose == 3:
		# Logging level for -vvv
		loghandler.setLevel(logging.INFO)
		scriptlogger.setLevel(logging.INFO)
		scriptlogger.debug('Logging level set to INFO')
	else:
		# Logging level for -vvvv+
		loghandler.setLevel(logging.DEBUG)
		scriptlogger.setLevel(logging.DEBUG)
		scriptlogger.debug('Logging level set to DEBUG')

	# Set up the file Queue.
	scriptlogger.debug('Creating query log file queue')
	filequeue = Queue.Queue()

	# Set up the start and end range list if a range has been specified.
	namerangelist = None
	if options.epochstart and options.epochend:
		if options.epochinc:
			namerangelist = xrange(options.epochstart, options.epochend + 1,
				options.epochinc)
		else:
			namerangelist = xrange(options.epochstart, options.epochend + 1,
				DEFAULTINCREMENT)

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
		scriptlogger.critical('Error globbing %s', os.path.join(options.basedir,
			options.queryyear, options.querymonth,
			options.queryday))

	# Collect the total size of the file queue for status messages later
	MAXQUEUEDEPTH = filequeue.qsize()
	scriptlogger.info('Items queued: %d', MAXQUEUEDEPTH)

	# Set up the worker threads. One per CPU, or the number specified on the
	# command line.
	scriptlogger.debug('Spawning worker processes')
	for i in range(options.scriptthreads):
		# Create a process, point it at our dequeue function, and pass it
		# the queue of file items, the output file handle, and the zone to
		# search for.
		t = multiprocessing.Process(target=dequeue, args=(filequeue, queryoutput,
		options.queryzones,))

		# Daemonizing processes means the main program won't leave threads
		# running and quit.
		t.daemon = True

		# Calling start() makes the threads begin working as we create them.
		t.start()
	scriptlogger.debug('Done spawning worker processes')

	# Wait for the threads to finish working...
	while len(multiprocessing.active_children()) > 0:
		# If the queue is empty, the threads will quit on their own. So we only
		# care how many threads are still running. This prevents us from
		# beginning the cleanup & close processes while threads may still have
		# data to write.
		try:
			# While there are items in the queue and active threads, wait 1 sec.
			time.sleep(1)
		except KeyboardInterrupt:
			# There are items in the queue and threads running, but we've received
			# CTRL-C to quit the script.
			scriptlogger.critical('Caught ctrl-c. Stopping worker processes.')
			for p in multiprocessing.active_children():
				p.terminate()
			while len(multiprocessing.active_children()) > 0:
				# There are still threads running. Print a status message
				# and wait 1 sec for them to complete.
				# If there is a "hung" thread, this could easily loop forever
				# so there should probably be a final timeout.
				scriptlogger.info('Waiting for remaining processes to die... ' +
				str(len(multiprocessing.active_children())))
				time.sleep(1)
			# Exit the while loop. We don't care there's remaining work
			break

	scriptlogger.debug('Flushing output files')
	queryoutput.flush()
	queryoutput.close()
	scriptlogger.debug('Finished flushing output files')
	scriptlogger.debug('Finished processing query log queue')
