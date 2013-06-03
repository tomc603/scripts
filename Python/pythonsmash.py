#!/usr/bin/env python
###############################################################################
# PythonSmash
###############################################################################
# Description:
#	PyhonSmash is a network service exerciser. With it, you can test the 
#	performance limits of servers and the services they host.
#
#	Supported Services:
#		HTTP(s)
#		SMTP
#		DNS
#		Raw UDP
#		Raw TCP
#
# Author: Tom Cameron <tcameron@dyn.com>
#
###############################################################################
import optparse
import sys


###############################################################################
# Slave-mode functions
###############################################################################
def slaveConnectToMaster():
	"""Connect to a master-mode client"""
	try:
		print 'slaveConnectToMaster()'
	except KeyboardInterrupt:
		print 'slaveConnectToMaster() caught CTRL-C. Setting terminate flag.'
		e.set()

def slaveRegisterWithMaster():
	"""Register this slave-mode client with the master-mode client"""
	try:
		print 'slaveRegisterWithMaster()'
	except KeyboardInterrupt:
		print 'slaveRegisterWithMaster() caught CTRL-C. Setting terminate flag.'
		e.set()

def slaveSendStatus():
	"""Send status message to the master-mode client"""
	try:
		print 'slaveSendStatus()'
	except KeyboardInterrupt:
		print 'slaveSendStatus() caught CTRL-C. Setting terminate flag.'
		e.set()

def slaveSendResults():
	"""Send results to the master-mode client"""
	try:
		print 'slaveSendResults()'
	except KeyboardInterrupt:
		print 'slaveSendResults() caught CTRL-C. Setting terminate flag.'
		e.set()

def runSlaveMode():
	"""Run this instance as a slave to a master-mode client"""
	try:
		print 'runSlaveMode()'
	except KeyboardInterrupt:
		print 'runSlaveMode() caught CTRL-C. Setting terminate flag.'
		e.set()

###############################################################################
# Master-Mode functions
###############################################################################
def masterHandleSlaveConnect():
	"""Handle a slave-mode client connection initiation"""
	try:
		print 'masterHandleSlaveConnect()'
	except KeyboardInterrupt:
		print 'masterHandleSlaveConnect() caught CTRL-C. Setting terminate flag.'
		e.set()

def masterHandleSlaveRegistration():
	"""Handle a slave-mode client registering itself"""
	try:
		print 'masterHandleSlaveRegistration()'
	except KeyboardInterrupt:
		print 'masterHandleSlaveRegistration() caught CTRL-C. Setting terminate flag.'
		e.set()

def masterRequestSlaveStatus():
	"""Request a status message from a slave"""
	try:
		print 'masterRequestSlaveStatus()'
	except KeyboardInterrupt:
		print 'masterRequestSlaveStatus() caught CTRL-C. Setting terminate flag.'
		e.set()

def masterHandleSlaveStatus():
	"""Handle a slave-mode client's status messages"""
	try:
		print 'masterHandleSlaveStatus()'
	except KeyboardInterrupt:
		print 'masterHandleSlaveStatus() caught CTRL-C. Setting terminate flag.'
		e.set()

def masterRequestSlaveResults():
	"""Request a results message from a slave"""
	try:
		print 'masterRequestSlaveResults()'
	except KeyboardInterrupt:
		print 'masterRequestSlaveResults() caught CTRL-C. Setting terminate flag.'
		e.set()

def masterHandleSlaveResults():
	"""Handle a slave-mode client's results messages"""
	try:
		print 'masterHandleSlaveResults()'
	except KeyboardInterrupt:
		print 'masterHandleSlaveResults() caught CTRL-C. Setting terminate flag.'
		e.set()

def masterSetupSlave():
	"""Send test parameters to slave"""
	try:
		print 'masterSetupSlave()'
	except KeyboardInterrupt:
		print 'masterSetupSlave() caught CTRL-C. Setting terminate flag.'
		e.set()

def runMasterMode():
	"""Run this instance as a master-mode client"""
	try:
		print 'runMasterMode()'
	except KeyboardInterrupt:
		print 'runMasterMode() caught CTRL-C. Setting terminate flag.'
		e.set()

###############################################################################
# DNS functions
###############################################################################
def DnsTest(e, threads, server, query):
	"""Put a load on a DNS server"""
	try:
		print 'Spawn processes that query a DNS server'
	except KeyboardInterrupt:
		print 'DnsTest caught CTRL-C. Setting terminate flag.'
		e.set()

def DnsWorker(e, server, query):
	"""Repeatedly query a DNS server for the specified name"""
	try:
		print 'Query a DNS server'
	except KeyboardInterrupt:
		print 'DnsWorker module caught CTRL-C. Setting terminate flag.'
		e.set()

###############################################################################
# SMTP functions
###############################################################################
def SmtpTest(e, threads, address):
	"""Put a load on an SMTP server"""
	try:
		print 'Spawn processes that connect to an SMTP server'
	except KeyboardInterrupt:
		print 'SmtpTest caught CTRL-C. Setting terminate flag.'
		e.set()

def SmtpWorker(e, address):
	"""Repeatedly connect to an SMTP address"""
	try:
		print 'Connect to an SMTP server'
	except KeyboardInterrupt:
		print 'SmtpWorker module caught CTRL-C. Setting terminate flag.'
		e.set()

###############################################################################
# HTTP functions
###############################################################################
def HttpTest(e, threads, address):
	"""Put a load on an HTTP(s) server"""
	try:
		print 'Spawn processes that connect to a HTTP server'
	except KeyboardInterrupt:
		print 'HttpTest caught CTRL-C. Setting terminate flag.'
		e.set()

def HttpWorker(address, count=1000):
	"""Repeatedly connect to a HTTP address"""
	try:
		print 'Connect to a HTTP server'
	except KeyboardInterrupt:
		print 'HttpWorker module caught CTRL-C. Setting terminate flag.'
		e.set()

###############################################################################
# Script body
###############################################################################
if __name__ == '__main__':
	# Interpret command line parameters, spawn threads and processes to
	# handle connecting to the different services, and process their results.

	#
	# Basic variables and default values
	#
	SCRIPTVER = '0.2'

	try:
		#
		# Parse the command line arguments
		#
		optionparser = optparse.OptionParser(version=SCRIPTVER)

		# Specify the valid options available in the script, and the variables
		# to store their arguments in. Also provide a helpful description for each
		# option to be output when a user specifies '--help'.
		optionparser.add_option('-m', '--mode', default=None, dest='runmode',
			help='Mode to run this script in. Slave or Master')
		optionparser.add_option('-s', '--server', default=None, dest='server',
			help='Server to perform SMTP or DNS test against')
		optionparser.add_option('-q', '--query', default=None, dest='query',
			help='String to query DNS server for')
		optionparser.add_option('-t', '--test', default=None, dest='test',
			help='Perform the specified test. Values: http, smtp, dns')
		optionparser.add_option('-p', '--parallel', default=1, dest='parallel',
			help='Number of parallel workers to use')
		optionparser.add_option('-u', '--url', default=None, dest='url',
			help='URL to request from the specified server')
		options, args = optionparser.parse_args()

		# Test the parsed options
		if not options.runmode is None:
			# An operating mode was specified.
			if options.runmode.lower() is 'master'
				print '\nSTATUS: Running script in MASTER mode'
				ScriptMasterMode = True
			else
				print '\nSTATUS: Running script in SLAVE mode'
				ScriptMasterMode = False
		else:
			# An operating mode was not specified. Alert the user and quit.
			print '\nERROR: You MUST specify an operating mode.'
			optionparser.print_help()
			sys.exit(1)

		if not options.test is None:
			# A test mode was specified.
			if options.test.lower() in ['http', 'https']:
				if not options.url is None:
					print 'URL option specified:', options.url
					queryurl = urllib.quote(options.url, safe='/:?&=')
					HttpWorker(address=queryurl, count=1000)
				else:
					print '\nERROR: You MUST specify a URL to retrieve when ' + \
						'performing an HTTP(s) test!\n'
					optionparser.print_help()
					sys.exit(1)
		else:
			# A test mode was not specified. Alert the user and quit.
			print '\nERROR: You MUST specify a test to perform!\n'
			optionparser.print_help()
			sys.exit(1)
	except KeyboardInterrupt:
		print 'Main process caught CTRL-C. Setting terminate flag.'
		TerminateEvent.set()
