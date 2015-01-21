#!/usr/bin/python2.7

import requests
import json
import sys

apiToken = 'xoxp-2221380517-2264684006-2265842837-d2174c'
apiChannel = 'C026HB6FD' # general

slackHookToken = 'ITOPDLyrAemt2CMwyVwDCfnn'
slackHookChannel = '#thoughtleadercouncil'
slackHookName = 'ObamaBot'
slackHookmessage = 'You\'re welcome!'

jsonObject = json.dumps({'text': 'You\'re welcome <http://i.imgur.com/SR3Xocc.jpg>',
                         'channel': slackChannel,
                         'username': slackName})

payload = {'token': slackToken,
           'payload': jsonObject}

or = requests.post(('https://slack.com/api/channels.mark?token=%s&channel=%s&ts=1396488843' %
                   apiToken, apiChannel))

ir = requests.post(('https://dyn.slack.com/services/hooks/incoming-webhook?token=%s' % slackToken),
                data=payload)

print(ir.text)
