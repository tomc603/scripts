#!/usr/bin/env python

"""
	Walk the postfix queue directories looking for files. Store the last known
	queue counts in a pickled file.
"""

# Count variables
activeq = 0
incomingq = 0
deferredq = 0
maildropq = 0

