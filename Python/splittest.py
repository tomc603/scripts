#!/usr/bin/env python
__author__ = 'tcameron'

def searchlist(srcstr):
    returnset = set()

    splitstr = srcstr.split('.')
    for i in xrange(len(splitstr)):
        resultstr = '.'.join(splitstr[i:])
        returnset.add(resultstr)
    return returnset

fqdn = "some.long.host.name.com"
searchset = set()
for i in xrange(1000000):
    searchset = searchlist(fqdn)
print searchset
