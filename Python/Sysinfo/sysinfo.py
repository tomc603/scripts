#!/usr/bin/env python

# -*- coding: utf-8 *-*

import checks
import ConfigParser


def walkmod(mod, attr, modlist):
	"""Walk a tree of modules starting at 'mod' looking for modules that have
	the specified attribute 'attr'. Append the modules to the list 'modlist'."""
	try:
		for m in dir(mod):
			if not m.startswith('_'):
				print m
				walkmod(m, attr, modlist)
				if hasattr(m, attr):
					modlist.append(mod)
	except:
		pass


def striplist(l):
	"""Strip() each item in a list, returning the stripped list."""
	return([x.strip() for x in l])


def readconfig(conf, filelist):
	"""Read the contents of the config file list into the config object.

	This is split out to its own function so we can re-read the config at any
	time from any place."""
	conf.read(filelist)


# Read the config file to get a list of what we need to check
# an what values to check for.
configfiles = ['sysinfo.conf']
config = ConfigParser.SafeConfigParser()
readconfig(config, configfiles)

myUptime = checks.system.uptime.runchecks(config)

print 'Uptime:', myUptime
