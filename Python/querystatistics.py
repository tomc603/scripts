#!/usr/bin/env python

#
# This script searches through DNS query log files for the specified zone name.
# The search is performed for a specified date entered on the comand line.
#
# TODO Arguments:
#


import bz2
import datetime
import glob
from cStringIO import StringIO
import logging
import md5
import optparse
import os
import Queue
import sys
import threading
import time
#import fnmatch
#import multiprocessing


def filecollector(q, o, searchzone, e):
	"""
		For the directory passed, find all files in the glob beneath it and
		add it to the queue 'q'.
		If e.isSet() is True, we need to exit the thread.
	"""
	scriptlogger.debug('filecollector doesn\'t do anything yet.')


def topn(filedata, num):
	"""
		Given the data 'filedata', output the top 'num' query consumers

		Return the top N in a dictionary, with the zone as the key, and the
		query count as the value.
	"""


def zonetopregion(filedata, zone):
	"""
		Given the data 'filedata', output the regional query count for the zone
		'zone'

		Return the regional query counts in a dictionary, with the region as
		the key, and the query count as the value.
	"""


def regiontopnzone(filedata, region, num):
	"""
		Given the data 'filedata', output the top 'num' query consumers for the
		region 'region'

		Return the top N in a dictionary, with the zone as the key, and the
		query count as the value.
	"""


def dequeue(q, o, searchzone, e):
	"""
		Process each file in the queue 'q', searchinf for the zone 'searchzone'.
		If e.isSet() is True, we need to exit the thread.
	"""
	global SERVERHASHDICT
	while not q.empty():
		if e.isSet():
			scriptlogger.debug('Break signal caught. Breaking out of loop.')
			break
		try:
			# Using threading.local() makes variables and data local to
			# the current thread only. This prevents variable collision and
			# reduces the need for locking, which prevents the GIL from being
			# hammered on...hopefully.
			threaddata = threading.local()
			# StringIO() functions are extremely fast, which reduces the time
			# required to append log lines to our output collector.
			threaddata.outputlines = StringIO()
			# Fetch an item from the queue, and do not wait for an item to be
			# available. If one isn't available, we catch the exception below.
			threaddata.processitem = q.get(False)
			scriptlogger.info('[ %1.1f%% ]', float(q.qsize()) / float(MAXQUEUEDEPTH) * 100)
			scriptlogger.debug('Dequeueing file %s', threaddata.processitem)

			# Set a sane initial value for the file
			threaddata.f = None

			# Get the file extension so we know how to read real data from it
			threaddata.fileext = os.path.splitext(threaddata.processitem)[1]

			# Test the extension and process accordingly
			if threaddata.fileext == ".bz2":
				# The file found ends in .bz2. Use the python bzip2 handling
				# module to decompress and read the file into the variable 'f'.
				threaddata.f = bz2.BZ2File(threaddata.processitem, 'rb').readlines()
			else:
				# The file is assumed to be uncompressed text. This may be wrong,
				# but importing unneeded libraries like gzip is probably more
				# wrong.
				threaddata.f = open(threaddata.processitem).readlines()

			if threaddata.f != None:
				# If we have data in 'f'. Process it!
				for threaddata.line in threaddata.f:
					# Create a variable that contains the line split by white
					# space.
					threaddata.splitline = threaddata.line.strip().split()
					if threaddata.splitline[8].strip().endswith(searchzone):
						# If the 9th field contains the specified zone, process it
						if options.anonymize:
							# Override the server's name to anonymize our network.
							# The full server name should be in field #3
							threaddata.servername = threaddata.splitline[3]
							# Split the server's name on the '-' character
							threaddata.splitservername = threaddata.servername.split('-')
							# Retrieve the site name (ie. ewr, ams...)
							threaddata.sitename = ''.join(threaddata.splitservername[-1:])
							if not threaddata.servername in SERVERHASHDICT:
								# Instead of calculating the same MD5 for
								# every line with the same server name,
								# build a dictionary with the hash values
								# and save lots of CPU time.
								scriptlogger.debug('Server\'s hash not found ' +
									'in dictionary. Adding.')
								SERVERHASHDICT[threaddata.servername] = md5.new(threaddata.servername).hexdigest()
							threaddata.serverhash = str(SERVERHASHDICT[threaddata.servername])
							# Combine the MD5 and the site name for the new
							# server name in the output file
							threaddata.splitline[3] = threaddata.serverhash + '-' + threaddata.sitename
						# Append the query log line to the output variable
						threaddata.outputlines.write(' '.join(threaddata.splitline) + '\n')
			# Compress the output data in each thread to get the benefit
			# of multiple CPUs. Write output in big chunks so we don't beat
			# the storage to death
			o.write(bz2.compress(threaddata.outputlines.getvalue()))
			scriptlogger.debug('Marking queue item complete and cleaning up.')
			# Remove the processed item from the queue
			q.task_done()
		except Queue.Empty:
			# There are no more file items on the queue to process, but the
			# thread has been spawned anyway. This is common, so handle it
			# gracefully.
			scriptlogger.debug('File queue is empty')


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
	# Empty dictionary to contain server name hashes
	SERVERHASHDICT = {}
	# Default CPU count for subsequent thread count
	CPUCOUNT = 0

	# Figure out the number of processors, and use that later
	# to start up CPUCOUNT threads by default
	ncpus = os.sysconf("SC_NPROCESSORS_ONLN")
	if isinstance(ncpus, int) and ncpus > 0:
		CPUCOUNT = ncpus

	# multiprocessing only exists in Python 2.6+. It was backported to
	# previous versions, but it's best to not rely on that kind of thing
	# for systems of unknown age.
	#CPUCOUNT = multiprocessing.cpu_count()
	MAXQUEUEDEPTH = 0

	# By default, output query log lines to STDOUT
	queryoutput = sys.stdout

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
	optionparser = optparse.OptionParser(usage='%prog [options] -b /some/log/dir -z example.com',
		version=SCRIPTVER)

	# Specify the valid options available in the script, and the variables
	# to store their arguments in. Also provide a helpful description for each
	# option to be output when a user specifies '--help'.
	optionparser.add_option('-a','--anon', default=False, dest='anonymize',
		action='store_true',
		help='Anonymize internal host data. Default: False.')
	optionparser.add_option('-b','--basedir', default='.', dest='basedir',
		help='Base directory to perform query log search in. Default: Current directory.')
	optionparser.add_option('-c','--compress', default=False,
		dest='compressquerylog', action='store_true',
		help='Compress the output query log file. Automatically adds .bz2 extension. Default: False.')
	optionparser.add_option('-d','--day', default=YESTERDAY.day,
		dest='queryday', type=int,
		help='Day to perform query log search on. Default: Yesterday')
	optionparser.add_option('-e','--end', default=None, dest='epochend',
		type=int, help='Epoch timestamp of the last log file. Default: None')
	optionparser.add_option('-f','--file', default='*', dest='queryfilefilter',
		help='Filter to narrow query files down. Default: *')
	optionparser.add_option('-i','--increment', default=None, dest='epochinc',
		type=int, help='Number to increment timestamp by. Default: None')
	optionparser.add_option('-l','--log', default=None, dest='scriptlogfile',
		help='Log file for script messages. Default: STDERR')
	optionparser.add_option('-m','--month', default=YESTERDAY.month,
		dest='querymonth', type=int,
		help='Month to perform query log search on. Default: Yesterday')
	optionparser.add_option('-o','--output', default=None,
		dest='queryoutputfile',
		help='Log file for query entries found. Default: zone.YYYY-MM-DD.log')
	optionparser.add_option('-s','--start', default=None, dest='epochstart',
		type=int, help='Epoch timestamp of the first log file. Default: None')
	optionparser.add_option('-t','--threads', default=CPUCOUNT,
		dest='scriptthreads', type=int,
		help='Threads to use for query log processing. Default: CPU count')
	optionparser.add_option('-v','--verbose', default=0, dest='scriptverbose',
		action='count', help='Increase verbosity this script should have 0-5. Default: 0')
	optionparser.add_option('-y','--year', default=YESTERDAY.year,
		dest='queryyear', type=int,
		help='Year to perform query log search on. Default: Yesterday')
	optionparser.add_option('-z','--zone', default=None, dest='queryzone',
		help='Zone name to find in query logs. Default: None (All)')

	# Parse the options and arguments passed on the command line
	options, args = optionparser.parse_args()

	# Output some parameter values for verification when debugging
	scriptlogger.debug('Finished processing CLI options')
	scriptlogger.debug('Verbose level: %s', options.scriptverbose)
	scriptlogger.debug('Base dir: %s', options.basedir)
	scriptlogger.debug('Zone: %s', options.queryzone)
	scriptlogger.debug('Script log: %s', options.scriptlogfile)
	scriptlogger.debug('Script output: %s', options.queryoutputfile)
	scriptlogger.debug('Thread count: %d', options.scriptthreads)
	scriptlogger.debug('Day: %d', options.queryday)
	scriptlogger.debug('Month: %d', options.querymonth)
	scriptlogger.debug('Year: %d', options.queryyear)

	#
	# Check option sanity and assign values for script parameters
	#
	if not glob.glob(options.basedir):
		# The glob of basedir isn't returning anything! Bail out to be safe.
		scriptlogger.critical('Please check the basedir parameter! ' +
		'No subdirectories returned!')
		sys.exit(1)

	if not glob.glob(options.basedir + '/' + str(options.queryyear)):
		# The glob of basedir and year isn't returning anything!
		# Bail out to be safe.
		scriptlogger.critical('Please check the year parameter! ' +
		'No subdirectories returned!')
		sys.exit(1)

	if not glob.glob(options.basedir + '/' + str(options.queryyear) +
		'/' + str(options.querymonth)):
		# The glob of basedir, year, and month isn't returning anything!
		# Bail out to be safe.
		scriptlogger.critical('Please check the month parameter! ' +
		'No subdirectories returned!')
		sys.exit(1)

	if not glob.glob(options.basedir + '/' + str(options.queryyear) + '/' +
		str(options.querymonth) + '/' + str(options.queryday)):
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

	if not options.queryzone:
		# No zone was specified, so we have nothing to search for!
		# Inform the user and bail out to be safe.
		scriptlogger.critical('You must specify a zone!')
		sys.exit(1)

	if options.queryoutputfile:
		# An output file for query logs has been specified
		try:
			if options.compressquerylog:
				# We are logging to a compressed file. Add the proper extension
				# and specify a buffer size to reduce IO operations on disk hardware.
				scriptlogger.debug('Compressing query log output file')
				queryoutput = open(options.queryoutputfile + '.bz2',
				mode='w', buffering=BUFFSIZ)
			else:
				# We are logging plain text. Specify a buffer size to reduce
				# IO operations on disk hardware.
				queryoutput = open(options.queryoutputfile, mode='w', buffering=BUFFSIZ)
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

	# Process each directory found by glob.glob
	# This could be sped up by making a threaded file searcher- one thread per
	# directory returned by glob.glob(). For now, it's fast enough using
	# the walk() function.
	try:
		for globdir in glob.glob(os.path.join(options.basedir,
			str(options.queryyear), str(options.querymonth),
			str(options.queryday))):
			for (dirpath, dirnames, filenames) in os.walk(globdir):
				for datafile in filenames:
					filequeue.put(os.path.join(dirpath, datafile))
					scriptlogger.debug('[%d] Queueing file %s', filequeue.qsize(), os.path.join(dirpath, datafile))
	except:
		scriptlogger.error('Error globbing %s', os.path.join(options.basedir,
			str(options.queryyear), str(options.querymonth),
			str(options.queryday)))

	# Collect the total size of the file queue for status messages later
	MAXQUEUEDEPTH = filequeue.qsize()
	scriptlogger.info('Items queued: %d', MAXQUEUEDEPTH)

	# Create an event that will signal threads to stop processing the queue
	quitevent = threading.Event()

	# Set up the worker threads. One per CPU, or the number specified on the
	# command line.
	scriptlogger.debug('Spawning worker threads')
	for i in range(options.scriptthreads):
		# Create a thread, point it at our dequeue function, and pass it
		# the queue of file items, the output file handle, the zone to search
		# for, and the event to watch to enable quitting upon user request.
		t = threading.Thread(target=dequeue, args=(filequeue, queryoutput,
		options.queryzone, quitevent,))

		# Daemonizing threads means the main program won't leave threads
		# running and quit.
		t.daemon = True

		# Calling start() makes the threads begin working as we create them.
		t.start()
	scriptlogger.debug('Done spawning worker threads')

	# Wait for the threads to finish working...
	while not filequeue.empty() and len(threading.enumerate()) > 1:
		try:
			# While there are items in the queue and active threads, wait 1 sec.
			time.sleep(1)
		except KeyboardInterrupt:
			# There are items in the queue and threads running, but we've received
			# CTRL-C to quit the script.
			scriptlogger.critical('Caught ctrl-c. Stopping worker threads.')
			# Set the event flag to tell our threads to quit.
			quitevent.set()
			while len(threading.enumerate()) > 1:
				# There are still threads running, wait 1 sec for them to complete
				scriptlogger.info('Waiting for remaining threads to die... ' +
				str(len(threading.enumerate()) - 1))
				time.sleep(1)
			# Exit the while loop. We don't care there's remaining work
			break

	scriptlogger.info('Unique hostnames found: %d', len(SERVERHASHDICT))
	scriptlogger.debug('Flushing output files')
	if not options.compressquerylog:
		# bz2 module doesn't support flush(). Otherwise, flush() to be safe.
		queryoutput.flush()
	queryoutput.close()
	scriptlogger.debug('Finished flushing output files')
	scriptlogger.debug('Finished processing query log queue')
