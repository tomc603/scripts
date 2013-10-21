#!/usr/bin/env python

import cStringIO
from zope.interface import implements
from twisted.internet import reactor
from twisted.mail import smtp
from twisted.mail.imap4 import LOGINCredentials, PLAINCredentials


class ProcessedMessageDelivery:
    implements(smtp.IMessageDelivery)

    def receivedHeader(self, helo, origin, recipients):
        return "Received: ProcessedMessageDelivery"

    def validateFrom(self, helo, origin):
        return origin

    def validateTo(self, user):
        if user.dest.local == "console":
            return lambda: ConsoleMessage()
        raise smtp.SMTPBadRcpt(user)


class CustomerMessage:
    implements(smtp.IMessage)

    def __init__(self):
        self.lines = cStringIO.StringIO()

    def lineReceived(self, line):
        self.lines.write(line)

    def eomReceived(self):
        print('New message:s')
        self.lines.close()
        return defer.succeed(None)

    def connectionLost(self):
        self.lines.close()


class CustomerSMTPFactory(smtp.SMTPFactory):
    protocol = smtp.ESMTP

    def __init__(self, *a, **kw):
        smtp.SMTPFactory.__init__(self, *a, **kw)
        self.delivery = ProcessedMessageDelivery()

    def buildProtocol(self, addr):
        p = smtp.SMTPFactory.buildProtocol(self, addr)
        p.delivery = self.delivery
        p.challengers = {"LOGIN": LOGINCredentials, "PLAIN": PLAINCredentials}
        return p


reactor.listenTCP()

a = service.Application("Console SMTP Server")
internet.TCPServer(25, CustomerSMTPFactory(portal)).setServiceParent(a)
