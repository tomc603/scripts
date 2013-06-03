#!/usr/bin/env python

from twisted.web.client import getPage


def got_page(data):
	"""Display a page that we received"""
	print 'Got a page\n', data

deferred = getPage('http://www.google.com')
deferred.addCallback(got_page)
