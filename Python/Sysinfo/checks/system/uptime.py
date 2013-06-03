# -*- coding: utf-8 *-*

import sys


def runchecks(conf):
	"""Return the appropriate uptime value in seconds"""

	osname = sys.platform
	if osname.startswith('FreeBSD'):
		uptime = 1
	elif osname.startswith('Linux'):
		uptime = 2
	else:
		uptime = None

	return uptime
