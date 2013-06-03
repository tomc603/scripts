#!/usr/bin/env python

import datetime
import bz2
import re


class ZoneStat():
    def __init__(self):
        pass


def regexSearch():
    """Garbage Docstring"""
    fdata = bz2.BZ2File('/home/tcameron/tmp/2012/8/28/1346197200.bz2', 'rb').readlines()

    domList = ['twitter.com', 'amazon.com', 't.co', 'fastly.com', 'dyndns.com']
    gre = re.compile(r'^(?P<date>.*\s.*\s.*)\s(?P<hostname>.*)\s(?:.*)\s(?:.*)\s(?P<srcaddr>.*)\s(?:.*)\s(?P<fqdn>.*)\s'
                     r'(?P<request>.*)\s(?P<rrtype>.*)\s(?P<queryflags>.*)$')
    romregex = '(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)'
    #'^.*query\:\s(.*\.|)(' + '|'.join(domList) + ').*$'
    domrg = re.compile(romregex, re.IGNORECASE | re.DOTALL)

    startTime = datetime.datetime.now()
    outputLines = []
    for fileline in fdata:
        if domrg.search(fileline):
            outputLines.append(fileline)
    endTime = datetime.datetime.now()
    print('Runtime (sec):', (endTime - startTime).total_seconds())
    print(len(outputLines))
    return outputLines


def forSearch():
    """Garbage Docstring"""
    fdata = bz2.BZ2File('/home/tcameron/tmp/2012/8/28/1346197200.bz2', 'rb').readlines()

    biglist = ['amazon.com', 'ad4game.com', 'twimg.com', 'box.net',
               'twitter.com', 'extremereach.com', 'wooga.com', 'infolinks.com',
               'slnservice.net', 'slashdot.org']

    domList = biglist[:i]
    starttime = datetime.datetime.now()
    outputlines = []
    for fileline in fdata:
        splitline = fileline.lower().rsplit(None, 4)
        for domname in domList:
            domfield = splitline[1]
            if (domfield.endswith('.' + domname)) or (domfield == domname):
                outputlines.append(fileline)
    endtime = datetime.datetime.now()
    return (endtime - starttime).total_seconds()


if __name__ == '__main__':
    print('\nFor loop search')
    for i in xrange(1, 11):
        totaltime = 0L
        print 'Domain count:', i
        for c in xrange(0, 3):
            runtime = forsearch()
            print 'Runtime (sec):', runtime
            totaltime += runtime
        print 'Avg:', totaltime / 3, '\n'
