#!/usr/bin/python

# Copyright 2012 Dyn Inc. All Rights Reserved.
#
# Author:        Tom Cameron (tcameron@dyn.com)
# Last Modified: 2012/06/06
#

import sys
import os, os.path
import logging
import threading
import time
from datetime import datetime

DEFAULT_DNS_SERVER = "127.0.0.1"
DEFAULT_DNS_PORT = 53
DEFAULT_QUERY_TIMEOUT = 500
DEFAULT_QUERY_TYPE = "ANY"
DEFAULT_CONCURRENCY = 20
DEFAULT_RATE = 1000
DEFAULT_REPORT_RATE = 5

def parse_cmdline():
	from optparse import OptionParser
	
	parser = OptionParser(usage="usage: %prog [options]")
	
	#
	# DNS & Query options
	#
	parser.add_option("-t", "--target", dest="target_host", default=DEFAULT_DNS_SERVER, metavar="HOST",
	                  help="DNS server to benchmark (default: %s)" % DEFAULT_DNS_SERVER)
	parser.add_option("-p", "--port", dest="target_port", default=DEFAULT_DNS_PORT, metavar="PORT", type="int",
	                  help="DNS server port (default: %d)" % DEFAULT_DNS_PORT)
	parser.add_option("-w", "--timeout", dest="query_timeout", default=DEFAULT_QUERY_TIMEOUT, metavar="QUERYTIMEOUT",
	                  type="int", help="msec before a request is considered timed out (default: %d)" % DEFAULT_QUERY_TIMEOUT)
	parser.add_option("-q", "--type", dest="query_type", default=DEFAULT_QUERY_TYPE, metavar="QUERYTYPE",
	                  help="DNS query type (default: %s)" % DEFAULT_QUERY_TYPE)
	parser.add_option("-R", "--recursive", dest="query_recursive", default=False, action="store_true",
	                  help="Enable recursive flag in queries")
	parser.add_option("-c", "--count", dest="query_count", metavar="QUERYCOUNT", type="int",
	                  help="Stop after COUNT queries")
	
	#
	# Domain options
	#
	# TODO: Convert name to accept a list
	parser.add_option("-n", "--name", dest="query_name", action="append", default=None, metavar="QUERYNAME",
	                  help="Domain to query")
	parser.add_option("-f", "--file", dest="query_file", metavar="QUERYFILE",
	                  help="File containing a list of domains to query")
	
	#
	# Rate limiting options
	#
	parser.add_option("-C", "--threads", dest="query_threads", default=DEFAULT_CONCURRENCY, metavar="QUERYTHREADS",
	                  type="int", help="Number of parallel threads to use (default: %d)" % DEFAULT_CONCURRENCY)
	parser.add_option("-r", "--rate", dest="query_rate", default=DEFAULT_RATE, metavar="QUERYRATE", type="int",
	                  help="Rate of queries in QPS (default: %d)" % DEFAULT_RATE)
	parser.add_option("-a", "--report", dest="report_rate", default=DEFAULT_REPORT_RATE, metavar="REPORTRATE",
	                  type="int", help="Seconds between reports (default: %d)" % DEFAULT_REPORT_RATE)
	
	#
	# General options
	#
	parser.add_option("-v", "--verbose", action="store_const", const=logging.INFO,
	                  dest="log_level", default=logging.WARN, help="Output more status information while running")
	parser.add_option("--output", dest="log_file", metavar="FILE",
	                  help="File to log results")
	
	opts, args = parser.parse_args()
	return opts, args

class DNSBenchmark(object):
	def __init__(self, max_concurrency=20):
		self.lock = threading.Semaphore(max_concurrency)
	
if __name__ == '__main__':
	opts, args = parse_cmdline()
	
	# TODO:
	#  Call the working function in the DNSBenchmark class
	#  http://code.google.com/p/asyncdns/source/browse/trunk/demo/alexa.py
