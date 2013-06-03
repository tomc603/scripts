#!/usr/bin/env python

import re
#import sys

#srcfile = open(sys.argv[1])

# Sample line:
# Jul 13 21:05:01 host-01-hkg named[3470]: client 61.220.9.47#14863: query:
#	t.co IN A -ED

txt = 'Jul 13 21:05:01 dns4-01-hkg named[3470]: ' + \
	'client 61.220.9.47#14863: query: twitter.com IN A -ED\n' + \
	'Jul 13 21:05:02 dns4-01-hkg named[3470]: ' + \
	'client 61.220.9.48#14863: query: www.amazon.com IN A -ED\n'

# Separators
space = '\\s+'
colon = '\\:'
hashtag = '#'

# Syslog Date
datere = '((?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|' + \
	'Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Sept|Oct(?:ober)?|' + \
	'Nov(?:ember)?|Dec(?:ember)?)\s\\d+\s(?:(?:[0-1][0-9])|(?:[2][0-3])|' + \
	'(?:[0-9])):(?:[0-5][0-9])(?::[0-5][0-9])?(?:\\s?(?:am|AM|pm|PM))?)'

# Hash / Hostname
hostre = '([\w-]+)'

# Daemon
daemonre = '((?:[a-z][a-z]+))'

# PID
pidre = '(\\[.*?\\])'

# Client
clientre = '((?:[a-z][a-z]+))'

# IPv4 IP Address 1
addrre = '((?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.)' + \
	'{3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))(?![\\d])'

# Port number
portre = '(\\d+)'

# Action
actre = '\squery:\s'

# Query text
domlist = ['amazon.com', 'twitter.com', 't.co']
domre = '.*(' + '|'.join(domlist) + ')'
print 'Domain RE:', domre

#rg = re.compile(datere + space + hostre + space + daemonre + pidre + \
#	colon + space + clientre + space + addrre + hashtag + portre + colon + \
#	space + actre + colon + space + domre, re.IGNORECASE | re.DOTALL)

rg = re.compile('(^.*' + actre + domre + '\s.*)$', re.IGNORECASE | re.DOTALL)

m = rg.findall(txt)
#if m:
#	action = m.group(1)
#	domain = m.group(2)
#	flags = m.group(3)

#	print "(" + action + ")" + "(" + domain + ")" + "(" + flags + ")"
