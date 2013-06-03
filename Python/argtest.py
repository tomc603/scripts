#!/usr/bin/env python

import sys

print 'Argv len:', len(sys.argv) - 1
if len(sys.argv) > 1:
	for av in sys.argv[1:]:
		print av
