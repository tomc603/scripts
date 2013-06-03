Graphite
========

Description
-----------

Graphite is a framework used to interact with the Graphite graphing system.
The framework is capable of submitting data to and retrieving data from a
Graphite server, and exposes exceptions in an easy to handle way.

Prerequisites
-------------

Graphite has been written on Python 2.7. It should operate under on
Python 2.6, however.

No additional dependencies are required outside of the standard Python
libraries csv, json, socket, urllib, and urllib2.


Exceptions
==========
Graphite.ConnectionError
------------------------
Raised when a socket error or urllib2 error is encountered. The error message
passed in the exception will describe the error that occurred.

Graphite.DataFormatError
------------------------
Raised when Graphite data can not be manipulated into the requested format or
when the requested data can not be inserted into a DataPoint or DataRequest field.

Error
------------------------
Raised when an unhandled exception is encountered in the Graphite module.


Examples
=========

Submitting data
---------------
Some simple example code to submit data::

import Graphite

# Create an object that represents a Graphite server
srv = Graphite.Server(address='graphite.address.com')

# Create an object that represents a request for data from a Graphite server
# Note: dpName can be a string or a list of strings
dr = Graphite.DataRequest(dpName=['tcameron.test.framework.1', 'tcameron.test.framework.2'], dpFrom='-2days', dpUntil='-1days')

# Retrieve the data described by the request object and return it in CSV format
csvdata = srv.getCSV(dr)

# Iterate through the returned data and print each CSV line
for d in csvdata:
	print d


Requesting data
---------------
Some simple example code to request data::

import getpass
import Graphite

# Create an object that represents a Graphite server
#
# If you do not specify a password, but you do specify a username,
# creating a Server object will prompt you to interactively enter a password
# with a getpass() prompt.
srv = Graphite.Server(address='graphite.address.com', username='tcameron',
	password=getpass.getpass())

# Create a DataPoint object that contains the target name, value to submit,
# and the time to submit it for.
#
# By default dpTime will be set to time.time()
dp = Graphite.DataPoint(dpName='tcameron.test.framework.1', dpTime=time.time(),
	dpValue=123456789)

# Initiate a connection to the Graphite server.
#
# This will also happen automatically when you execute Graphite.Server().submit().
# But calling connect() seperately can allow cleaner error handling.
srv.connect()

# Submit the DataPoint object to the Graphite server.
#
# Server().submit() can send a single DataPoint or a list of DataPoint objects
srv.submit(dp)

# Shutdown and close the connection to the Graphite server
#
# After calling Server().close(), the socket is completely destroyed.
# Server().connect() will need to be called again to establish a connection.
# Calling Server().close() on a closed connection will result in an Exception.
srv.close()

