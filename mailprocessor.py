#!/usr/bin/env python

import email
import getpass
import imaplib
import time

FolderName = 'INBOX/Nagios Alerts'
TimeFormat = '%a, %d %b %Y %H:%M:%S %Z'

# Create the IMAP server and log in
M = imaplib.IMAP4_SSL('mail.google.com')
M.login(getpass.getuser(), getpass.getpass())

# Open the proper folder
M.select(FolderName)

# Search for messages
search_rcode, search_msg_id_list = M.search(None,
    '(SENTBEFORE 22-Jun-2013 SENTSINCE 20-Jun-2013)')

for msg_id in search_msg_id_list[0].split():
    fetch_rcode, fetch_data = M.fetch(msg_id, '(RFC822)')

    if 'OK' in fetch_rcode:
        message_parser = email.Parser.Parser()
        parsed_message = message_parser.parsestr(fetch_data[0][1])

    if 'PROBLEM' in parsed_message['Subject']:
        alertstr = parsed_message['Subject'].replace('**', '')
        alertstr = alertstr.replace('PROBLEM alert -', '')
        alertstr = alertstr.strip()
        timestr = time.strftime('%Y-%m-%d %H:%M:%S UTC', time.strptime(
            parsed_message['Date'], '%a, %d %b %Y %H:%M:%S %Z'))
        print('%s - %s' % (timestr, alertstr))
        #print('%s\n' % parsed_message.get_payload())
