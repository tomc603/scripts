#!/usr/bin/env python

from optparse import OptionParser
import dns.resolver
import dns.query
import dns.zone


def querytest(server, domain):
	'''
		Description: Query a name from a server.
	'''
	# Lookup MX records for a domain
	answers = dns.resolver.query('dnspython.org', 'MX')
	for rdata in answers:
		print 'Host:', rdata.exchange, 'has preference', rdata.preference
	return 0


def xfertest(server, domain):
	'''
		Description: Test xfer for a domain from a server.
	'''
	z = dns.zone.from_xfr(dns.query.xfr('204.152.189.147', 'dnspython.org'))
	names = z.nodes.keys()
	names.sort()
	for n in names:
		print z[n].to_text(n)
	return 0


def updatetest(server, domain):
	'''
		Description: Query a name from a server.
	'''
	return 0


def main():
	'''
		Description: Body of the script, responsible for calling the tests
		requested on the command line.
	'''
	parser = OptionParser()
	parser.add_option('-s', '--server', dest='dnsserver', default='127.0.0.1', \
		help='Specify a server to perform tests against')
	parser.add_option('-d', '--domain', dest='domain', default='sometest.com', \
		help='Specify a domain to perform tests against')
	parser.add_option('-x', '--xfer', dest='xfertest', action='store_true', \
		default=False, help='Perform an xfer test against a server for a domain')
	parser.add_option('-q', '--query', dest='querytest', action='store_true', \
		default=False, help='Perform a query test against a server for a domain')
	parser.add_option('-u', '--update', dest='updtetest', action='store_true', \
		default=False, help='Perform an update test against a server for a domain')
	(options, args) = parser.parse_args()


	# Which test to perform. Multiple tests may not be run at the same time,
	# so this is an OR, not an AND test.
	if options.xfertest:
		xfertest(server=options.dnsserver, domain=options.domain)
	elif options.querytest:
		querytest(server=options.dnsserver, domain=options.domain)
	elif options.updatetest:
		updatetest(server=options.dnsserver, domain=options.domain)


if __name__ == "__main__":
	main()
