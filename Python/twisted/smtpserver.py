#!/usr/bin/env python

__author__ = 'tcameron'

import sys
from cStringIO import StringIO

from email.header import Header
from zope.interface import implements

from twisted.internet import defer, reactor
from twisted.mail import smtp
# from twisted.python import log


class ProcessedMessageDelivery(object):
    implements(smtp.IMessageDelivery)

    def __init__(self, protocol):
        self.protocol = protocol

    def receivedHeader(self, helo, origin, recipients):
        clientHostname, _ = helo
        myHostname = self.protocol.transport.getHost().host
        headerValue = 'from %s by %s with ESMTP ; %s' % (clientHostname,
                                                         myHostname,
                                                         smtp.rfc822date())
        return 'Received: %s' % Header(headerValue)

    def validateFrom(self, helo, origin):
        return origin

    def validateTo(self, user):
        if user.dest.domain == 'example.com':
            return ProcessedMessage
        else:
            log.msg('Received email for invalid recipient %s' % user)
            raise smtp.SMTPBadRcpt(user)


class ProcessedMessage(object):
    implements(smtp.IMessage)

    def __init__(self):
        # self.lines = StringIO()
        self.lines = []

    def lineReceived(self, line):
        # self.lines.write(line)
        self.lines.append(line)

    def eomReceived(self):
        #log.msg('EOM received.')
        # self.lines.getvalue()
        # self.lines.close()
        ''.join(self.lines)
        self.lines = None
        return defer.succeed(None)

    def connectionLost(self):
        self.lines.close()
        # self.lines = None


class ProcessedMessageFactory(smtp.SMTPFactory):
    def buildProtocol(self, addr):
        proto = smtp.ESMTP()
        proto.delivery = ProcessedMessageDelivery(proto)
        return proto


#log.startLogging(sys.stdout)
# Source to script
# cStringIO: 625
# List IO  : 666.666666667

reactor.listenTCP(2500, ProcessedMessageFactory())
reactor.run()
