#!/usr/bin/env python
__author__ = 'tcameron'

import sys

from email.mime.text import MIMEText

from twisted.internet import reactor
from twisted.mail.smtp import sendmail
from twisted.python import log

log.startLogging(sys.stdout)

host = '127.0.0.1'
sender = 'source@example.com'
recipients = ['sink@example.com']

msg = MIMEText('''This is a long test message. Its content is total garbage,
 but the length is necessary to actually create queue files of a significant
 size. This should also put a load on system RAM, since messages are naively
 queued as strings in memory and not mmapped from queue files. Hooray!

If we're not careful, though, a client or server that has many message objects
 in memory could trigger the OOM killer to terminate it. But that will only
 happen after all of the system's swap and most of the RAM are consumed.

Also, beware of Linux's reserved memory. This causes lots of people to be
confused, because they see -free- memory, but it isn't really free. The OS
reserves it for processes running as root. Sadly, this isn't a fool-proof
plan because lots of processes run as root.

If you've ever run a database, MTA, or other user daemon as root in
production, you deserve whatever happens to you. Of course, the argument is
that each of these daemons require root permissions because they use a
service port number below 1024. That's total BS, though, because users can
be granted the right to use low-order ports.
''')

msg['Subject'] = 'Test message'
msg['From'] = 'Test Message Source <%s>' % sender
msg['To'] = ', '.join(recipients)

deferred = sendmail(host, sender, recipients, msg.as_string(), port=2500)
deferred.addBoth(lambda result: reactor.stop())

reactor.run()
