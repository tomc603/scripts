#!/usr/bin/env python

import commands
import ConfigParser
import os

#
# Create modules:
#  Checks
#    permissions
#      checkuid.py - Accounts with uid == 0
#      filepermissions.py - File permissions
#      nopassword.py - Accounts with no password
#      setuid.py - Setuid files & devices
#
#    mountpoints
#      checkspace.py - Avail. free space
#      zfs.py - ZFS & ZPOOL status
#
#    system
#      load.py - System load
#      mailq.py - Locally queued mail
#      ports.py - Checks for *BSD PORTS
#      uptime.py - System uptime
#
#    raid
#      3ware.py - 3ware hardware raid
#      amr.py - AMR hardware raid
#      linuxsoft.py - Linux software raid
#      mega.py - MegaRAID hardware raid
#      mfi.py - MFI hardware raid
#      mpt.py - MPT hardware raid
#
#    logs
#      auth.py - Errors in auth logs
#      cron.py - Errors in CRON logs
#      kernel.py - Errors in kernel logs
#      pfdenied.py - Denied traffic in pf logs
#      refused.py - Refused connection log
#


def striplist(l):
	"""Strip() each item in a list, returning the stripped list."""
	return([x.strip() for x in l])


def checkfreespace(cfg):
	"""Check free space for a list of mountpoints, or all mountpoints returned
	by 'mount -v'.

	Mountpoint list is read from ConfigParser 'cfg' as a comma seperated list
	or as a '*' to represent all mounted filesystems.

	A list of mountpoints to ignore may be specified in the config parameter
	'ignorelist'. A simple in check is performed for each mountpoint found,
	so the ignore list must be specific."""

	# Define our constraints
	MPLIST = striplist(cfg.get('freespace', 'mountpointlist').split(','))
	IGNORELIST = striplist(cfg.get('freespace', 'ignorelist').split(','))
	MINFREE = cfg.getint('freespace', 'minfreepcnt')

	# Define our defaults
	mountstats = {}
	mountpoints = MPLIST

	if '*' in MPLIST:
		# MPLIST contains a *, so we need to check all mounted filesystems
		# We don't care where in the list the * was found, which means we
		# ignore any other items contained in the list.
		print 'Checking all mounted FS'
		# Split the output of mount -v by lines
		mountlines = commands.getoutput('mount -v').split('\n')
		# Create a list containing the third field of each line from mountlines
		mountpoints = map(lambda line: line.split()[2], mountlines)

	for mountpoint in mountpoints:
		if not mountpoint in IGNORELIST:
			print 'Checking mountpoint:', mountpoint
			mountptstats = os.statvfs(mountpoint)
			if mountptstats.f_blocks > 0:
				# A device needs blocks to have blocks consumed. And since
				# divide by zero should turn the universe inside out, we'll
				# just skip any device that doesn't have a block count of 1 or
				# greater.
				pcntfree = float(mountptstats.f_bavail) / float(mountptstats.f_blocks) * 100
				if pcntfree < MINFREE:
					# The filesystem doesn't meet our minimum free space
					# requirement. Add it to a dictionary to be returned.
					mountstats[mountpoint] = pcntfree
			else:
				print 'Zero blocks in:', mountpoint
		else:
			print 'Ignoring mountpoint:', mountpoint

	# Return a dictionary of mountpoints that don't have enough free space.
	return mountstats


# Read the config file to get a list of what we need to check
# an what values to check for.
configfiles = ['sysinfo.conf']
config = ConfigParser.SafeConfigParser()
config.read(configfiles)

# Run our check functions
freespace = checkfreespace(config)

# Output anything over or under our constraints
for k in freespace.keys():
	print k, str(freespace[k])
