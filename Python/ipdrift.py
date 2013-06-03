#!/usr/local/bin/python

def FindInRegions(ipset):
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

def CountInInterval(ipset):
	print 'clientip,amsbefore,amsduring,amsafter,frabefore,fraduring,fraafter,lonbefore,londuring,lonafter'
	for clientip in ipset:
		outstr = clientip + ','
		for region in ['ams', 'fra', 'lon']:
			for querytime in ['before', 'during', 'after']:
				for searchline in open(region + '-' + querytime + '-topaddresses.log'):
					if clientip in searchline:
						outstr += searchline.split()[0]
				outstr += ','
		print outstr

clientipset = set()
for region in ['ams', 'fra', 'lon']:
	for line in open(region + '-before-topaddresses.log'):
		clientipset.add(line.split()[1])
	for line in open(region + '-during-topaddresses.log'):
		clientipset.add(line.split()[1])
	for line in open(region + '-after-topaddresses.log'):
		clientipset.add(line.split()[1])

print '\n\nIPs in Regions\n--------------'
FindInRegions(clientipset)

print '\n\nQueries in Regions by IP\n------------------------'
CountInInterval(clientipset)

