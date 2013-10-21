#!/usr/bin/env python
'''
    Create a pandas.Series() collection of data values to represent the data
    parsed from the sadf JSON export
'''

import json
import pandas as pds


#
# Data parsing functions
#
def DictToSeries(timeval, dataval):
    '''
        Convert the supplied dictionary 'dataval' into a data element to be
        inserted into a Pandas Series() at timeslot 'timeval'.

        @param timeval: Epoch representation of interval's collection time
        @type timeval: int?

        @param dataval: JSON data to convert
        @type dataval: dict or list of dict

        @return: Dictionary with key set to dataval's name, value set to a
                 pandas.Series() containing dataval's value
        @rtype: dict
    '''
    yield {'': False}

def ListToSeries(timeval, datalist):
    '''
        Iterate through each dictionary in 'datalist', passing it to
        DitcToSeries.

        @param timeval: Epoch representation of intervals' collection times
        @type timeval: int?

        @param dataval: JSON data to convert
        @type dataval: dict or list of dict

        @return: Dictionary with key set to dataval's name, value set to a
                 pandas.Series() containing dataval's value
        @rtype: dict

        Yields a list of Dict with key values of series name, and values of
        pandas.Series()
    '''
    yield [False]


def decodeTimestamp():
    """
    Receive a <timestamp></timestamp> element and parse it.

    Pull out the date, time, utc, and interval attributes
    Pass each child to its responsible function.

    @return:
    @rtype:
    """
    pass

def decodeCpuLoadAll():
    """
    Receive a <cpu-load-all></cpu-load-all> element and parse it.

    This element only contains child elements named <cpu />. Each <cpu />
    element contains the following attributes:
      * number - Int CPU number, or "all" for total
      * usr    - %CPU spent in application level
      * nice   - %CPU spent in application level w/nice priority.
      * sys    - %CPU spent in kernel level
      * iowait - %CPU spent with a disk I/O waiting
      * steal  - %CPU spent while hypervisor serviced other virt. CPU
      * irq    - %CPU spent servicing interrupts
      * soft   - %CPU spent servicing software interrupts
      * guest  - %CPU spent servicing virtual CPU
      * idle   - %CPU spent w/o task or disk I/O

    @return:
    @rtype:
    """
    pass

def decodeContextSwitch():
    """
    Receive a <process-and-context-switch /> element and parse it.

    Pull out per, proc, and cswch attributes.

    @return:
    @rtype:
    """
    pass


#
# Create an empty dict to store Series collection in
#
seriesdict = dict()


#
# Read the input JSON files
#
fname = 'gluster-02.sa02.json'
fhandle = open(fname, 'r')
rawdata = json.load(fhandle)
statdata = rawdata['sysstat']['hosts'][0]['statistics']


#
# Iterate through the intervals in the JSON file
#
# Iterate through each time interval
for datacollection in statdata:
    print '\nDate: %s @ %s' % (datacollection['timestamp']['date'], datacollection['timestamp']['time'])

    # Iterate through the stat types in this interval
    for datagroup in datacollection:
        '''
        Groups:
            kernel -> Dict
            network -> Dict
            timestamp -> Dict
            interrupts -> List
            queue -> Dict
            hugepages -> Dict
            power-management -> Dict
            process-and-context-switch -> Dict
            cpu-load-all -> List
            paging -> Dict
            io -> Dict
            memory -> Dict
            swap-pages -> Dict
            serial -> List
            disk -> List

        '''
        if type(datacollection[datagroup]) is list:
            print '%s -> List' % (datagroup)
        elif type(datacollection[datagroup]) is dict:
            print '%s -> Dict' % (datagroup)
        else:
            print '%s -> Unexpected' % (datagroup)

