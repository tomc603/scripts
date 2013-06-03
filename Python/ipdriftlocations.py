#!/usr/local/bin/python

clientipset = set()
for region in ['ams', 'fra', 'lon']:
	for line in open(region + '-before-topaddresses.log'):
		clientipset.add(line.split()[1])
	for line in open(region + '-during-topaddresses.log'):
		clientipset.add(line.split()[1])
	for line in open(region + '-after-topaddresses.log'):
		clientipset.add(line.split()[1])

for clientip in clientipset:
	foundlocations = list()
	for region in ['ams', 'fra', 'lon']:
		for querytime in ['before', 'during', 'after']:
			for searchline in open(region + '-' + querytime + '-topaddresses.log'):
				if clientip in searchline:
					foundlocations.append(region + ':' + querytime)
	if len(foundlocations) > 1:
		regstr = ''
		for regname in foundlocations:
			regstr += regname + ', '
		print clientip + ' found in: ' + regstr
