#!/usr/bin/env python

import bz2
import csv
import os
import re
import time


def in_gen(lines, domlist):
	"""
		Generator to return matching lines based on 'in'
	"""
	for line in lines:
		if line[8] in ['.' + x for x in domlist] or line[8] in domlist:
			yield line


def re_gen(lines, regexval):
	"""
		Generator to return matching lines based on regex search
	"""
	for line in lines:
		if recomp.search(line[8]):
			yield line


filelist = []
domlist = ['twitter.com', 'amazon.com', 'slashdot.org']
recomp = re.compile('(\S+\.|)' + '|'.join(domlist))
matchcount = 0

print 'Building file list'
stime = time.time()
for path, directories, files in os.walk('.'):
	filecomp = [curfile for curfile in files if curfile.endswith('.bz2')]
	for foundfile in filecomp:
		if len(filelist) < 10:
			filelist.append(os.path.join(path, foundfile))
		else:
			break
etime = time.time()
print 'Finished building file list', etime - stime

print 'Starting in processing'
stime = time.time()
for logfile in filelist:
	print 'Processing', logfile
	csvfile = csv.reader(bz2.BZ2File(logfile), delimiter=' ', \
		skipinitialspace=True)
	matches = in_gen(csvfile, domlist)
	for line in matches:
		line[3]
		matchcount += 1
etime = time.time()
print 'Finished in processing', matchcount, (etime - stime) / len(filelist)

print '\nStarting regex processing'
stime = time.time()
for logfile in filelist:
	print 'Processing', logfile
	csvfile = csv.reader(bz2.BZ2File(logfile), delimiter=' ', \
		skipinitialspace=True)
	matches = re_gen(csvfile, recomp)
	for line in matches:
		line[3]
		matchcount += 1
etime = time.time()
print 'Finished regex processing', matchcount, (etime - stime) / len(filelist)
