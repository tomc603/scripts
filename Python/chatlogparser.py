#!/usr/bin/env python

import sys
import datetime
from xml.dom.minidom import parse


def main():
	'''
		Description: Parse the chat log and print out the lines formatted
		with UTC time, or the raw time string from the file, the sender,
		and the text from the node itself.
	'''
	if len(sys.argv) > 1:
		for logfile in sys.argv[1:]:
			print 'Parsing', logfile
			logdom = parse(logfile)

			for node in logdom.getElementsByTagName('message'):
				msgtxt = ''
				chatname = ''
				timetxt = node.getAttribute('time')

				try:
					datestr = datetime.datetime.strptime(timetxt, '%Y%m%dT%H:%M:%S')
				except:
					datestr = timetxt

				try:
					chatname = node.getAttribute('name')
				except:
					chatname = 'Unknown'

				for cnode in node.childNodes:
					try:
						msgtxt += cnode.data
					except:
						msgtxt += 'Error reading XML node text.'
					if len(node.childNodes) > 1:
						msgtxt += '\n'

				try:
					if 'nagios' in chatname.lower():
						if (msgtxt.startswith('PROBLEM')) or (msgtxt.startswith('RECOVERY')):
							print datestr, 'UTC :', chatname, '->', msgtxt
				except:
					print 'Error printing log line!'

if __name__ == '__main__':
	main()
