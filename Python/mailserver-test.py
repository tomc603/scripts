import smtpd
import asyncore

class MySMTPServer(smtpd.SMTPServer):
    def __init__(self, *args, **kwargs):
        super(MySMTPServer, self).__init__(*args, **kwargs)
        self.rxcount = 0
    def process_message(self, peer, mailfrom, rcpttos, data):
        self.rxcount += 1
        if self.rxcount % 100 == 0:
            print('Rx Count:', self.rxcount)
        return

server = MySMTPServer(('127.0.0.1', 2525), None)
asyncore.loop()


