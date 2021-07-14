#!/usr/bin/python

import os
from optparse import OptionParser

totalsizestr = avgsizestr = ' '
totalfilecount = totalfailedfiles = 0
totalfilesize = largestfilesize = smallestfilesize = totalavgsize= calcfilesize = calcavgsize = 0.0

myoptionparser = OptionParser()
myoptionparser.add_option("-p", "--path", dest="path", help="Path to execute against", metavar="PATH")
(options, args) = myoptionparser.parse_args()

print "Gathering file information for", options.path

if options.path != None:
	for dirpath, dirnames, filenames in os.walk(options.path):
		for name in filenames:
			fullpath = os.path.join(dirpath, name)
			if os.access(fullpath, os.F_OK):
				totalfilecount += 1
				totalfilesize += os.lstat(fullpath).st_size
			else:
				totalfailedfiles += 1
	
	# Format the total file sizes
	if totalfilesize >= 1099511627776:
		calcfilesize = totalfilesize / 1099511627776
		totalsizestr = '%.2fT' % calcfilesize
	elif totalfilesize >= 1073741824:
		calcfilesize = totalfilesize / 1073741824
		totalsizestr = '%.2fG' % calcfilesize
	elif totalfilesize >= 1048576:
		calcfilesize = totalfilesize / 1048576
		totalsizestr = '%.2fM' % calcfilesize
	elif totalfilesize >= 1024:
		calcfilesize = totalfilesize / 1024
		totalsizestr = '%.2fK' % calcfilesize
	else:
		totalsizestr = '%.2fb' % totalfilesize
	
	# Calculate and format the average file sizes
	totalavgsize = totalfilesize / totalfilecount
	if totalavgsize >= 1099511627776:
		calcavgsize = totalavgsize / 1099511627776
		avgsizestr = '%.2fT' % calcavgsize
	elif totalavgsize >= 1073741824:
		calcavgsize = totalavgsize / 1073741824
		avgsizestr = '%.2fG' % calcavgsize
	elif totalavgsize >= 1048576:
		calcavgsize = totalavgsize / 1048576
		avgsizestr = '%.2fM' % calcavgsize
	elif totalavgsize >= 1024:
		calcavgsize = totalavgsize / 1024
		avgsizestr = '%.2fK' % calcavgsize
	else:
		avgsizestr = '%.2fb' % totalavgsize
	
	print '\nTotal files:', totalfilecount
	print 'Unreadable files:', totalfailedfiles
	print '\nTotal size:', totalsizestr
	print 'Avg. size:', avgsizestr
else:
	myoptionparser.print_help()
