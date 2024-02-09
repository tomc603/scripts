#!/usr/bin/env python3

import json

sites = {}
data = json.load(open('~/Documents/disks.json'))
try:
    for item in data:
        for content in item['content']:
            if 'SSDSC2KB019T8R' in content['product'] and 'DL63' in content['firmware_version']:
                sitename = item['host'].split('-')[1][:-2]
                if not sitename in sites.keys():
                    sites[sitename] = 0
                sites[sitename] = sites[sitename] + 1
except KeyError:
    pass
