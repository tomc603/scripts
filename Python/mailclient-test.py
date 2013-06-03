import smtplib
import email.utils
from email.mime.text import MIMEText

class Sender():                                                    
    def __init__(self, fromaddr, fromname, toaddr, toname, srvaddr, msgsubject, msgbody):
        self.fromaddr = fromaddr
        self.fromname = fromname
        self.toaddr = toaddr
        self.toname = toname
        self.srvaddr = srvaddr
        self.msgsubject = msgsubject
        self.msgbody = msgbody

        self.msg = MIMEText(self.msgbody)
        self.msg['To'] = email.utils.formataddr((self.toname, self.toaddr))
        self.msg['From'] = email.utils.formataddr((self.fromname, self.fromaddr))
        self.msg['Subject'] = self.msgsubject

        self.srv = smtplib.SMTP(self.srvaddr, 2525)
        self.srv.set_debuglevel(False)

    def send(self, sendcount):
        try:
            for i in range(sendcount):
                self.srv.sendmail(self.fromaddr, [self.toaddr], self.msg.as_string())
        except:
            print('Exception while sending message %d' % i)

    def quit(self):
        self.srv.quit()


snd = Sender('tomc603@gmail.com', 'Tom Cameron', 'tomc603@gmail.com', 'Tom Cameron', '127.0.0.1', 'Test message', 'This is the test message body. It is short and sweet.')

%%timeit
snd.send(800)

snd.quit()

