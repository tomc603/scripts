#!/usr/bin/env python

import random

def schedulePerson(namelist, startname=None):
    if not startname:
        startname = random.choice(namelist)

    initialindex = namelist.index(startname)
    curindex = initialindex

    while True:
        # Yield the current list item
        yield namelist[curindex]

        # If the next item would be past the end of the list, loop back to the
        # start of the list.
        if curindex == len(namelist) - 1:
            curindex = 0
        else:
            curindex += 1

if __name__ == '__main__':
    # List of people in the rotation
    ops = ['tom', 'tim', 'alex', 'neil', 'josh', 'david', 'liam', 'chip']

    # Number of days to print
    days = 15

    # Number of 24h days in a shift
    duration = 2

    # Start year, month, day of the on-call calendar
    startyear = 2013
    startmonth = 06
    startday = 10

    # Start date object
    startdate = datetime.datetime(startyear, startmonth, startday, 14)

    # Randomize the people list
    random.shuffle(ops)

    # Initialize a person generator for each on call level
    l1 = schedulePerson(ops, ops[2])
    l2 = schedulePerson(ops, ops[1])
    l3 = schedulePerson(ops, ops[0])

    # Print the on-call list!
    for c in xrange(days):
        sched_day = (l1.next(), l2.next(), l3.next())
        enddate = startdate + datetime.timedelta(days=duration)

        print('%s to %s:\n\tL1: %10s\n\tL2: %10s\n\tL3: %10s' %
            (startdate.isoformat(), enddate.isoformat(),
             sched_day[0], sched_day[1], sched_day[2]))
        startdate += datetime.timedelta(days=duration)
        print "\n"

