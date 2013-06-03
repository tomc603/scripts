#!/usr/bin/env python
from twisted.internet import reactor
import twisted.names.client

def do_lookup(do_lookup):
	d = twisted.names.client.lookupAllRecords(domain)
	d.addBoth(lookup_done)

def lookup_done(result):
	myresults = result
	for myresult in myresults:
		print '\nresult:', type(myresult), '\n', myresult
		for subresult in myresult:
			print '\nSubresult:', type(subresult), '\n', subresult
	reactor.stop()

domain = 'dyn.com'
reactor.callLater(0, do_lookup, domain)
reactor.run()
