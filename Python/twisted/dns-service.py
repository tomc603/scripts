#!/usr/bin/env python

# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

"""
Sample app to lookup SRV records in DNS.
To run this script:
$ python dns-service.py <service> <proto> <domain>

service =	the symbolic name of the desired service.
proto =		the transport protocol of the desired service; this is usually
			either TCP or UDP.
domain =	the domain name for which this record is valid.
e.g.:
$ python dns-service.py sip udp yahoo.com
$ python dns-service.py xmpp-client tcp gmail.com
"""

from twisted.names import client
from twisted.internet import reactor, defer
import sys

def printAnswer(answer):
	if not len(answer):
		print 'No answers'
	else:
		print 'Answer len:', len(answer)
		#print '\n'.join([str(x.payload) for x in answer])

def printFailure(arg):
	print "error: could not resolve:", arg

try:
	domain = sys.argv[1]
except ValueError:
	sys.stderr.write('%s: usage:\n' % sys.argv[0] +
		'  %s SERVICE PROTO DOMAIN\n' % sys.argv[0])
	sys.exit(1)

try:
	resolver = client.Resolver(servers=['172.16.12.127'])

	dl = defer.DeferredList([resolver.lookupAllRecords(domain, [1]) for i in
		xrange(2001)], consumeErrors=True)
	dl.addCallbacks(printAnswer, printFailure)

	# Stop running after 4 seconds.
	reactor.callLater(4, reactor.stop)

	# Start the reactor so the script does work.
	reactor.run()
except Exception, e:
	print 'Exception!', e

