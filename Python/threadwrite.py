#!/usr/bin/python

import optparse
import os
from Queue import Queue
import threading

def dequeue(threadname, logfile):
	#
	# Process each item on the queue in a thread
	#
	for i in range(128):
		logfile.write('[' + threadname + '] This is a test line ' + str(i) + '!\n')


outfile = open('test.log', 'w')
for i in range(8):
	t = threading.Thread(target=dequeue, args=('Thread-' + str(i), outfile,))
	t.daemon = True
	t.start()
