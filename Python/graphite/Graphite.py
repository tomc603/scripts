#===============================================================================
# Graphite.py
#===============================================================================
# Description:
# This module contains classes required to interact with Graphite
#===============================================================================
# Author:            Tom Cameron <tcameron@dyn.com>
# Last Modified:    2012-10-24 @ 20:49 UTC
#===============================================================================
"""
    The Graphite module simplifies interacting with a Graphite server by
    implementing a standard set of functions, data classes, and exceptions.
"""

#------------------------------------------------------------------------------
# Custom Exceptions
#------------------------------------------------------------------------------
class Error(Exception):
    """
        Base exception object for exceptions in this module
    """
    pass


class ConnectionError(Error):
    """
        Handle connection errors. Report the server name to the user.
    """
    pass


class DataFormatError(Error):
    """
        Handle data formatting errors. Report the specific issue to the user.
    """
    pass


#------------------------------------------------------------------------------
# Custom data containers
#------------------------------------------------------------------------------
class DataPoint():
    """
        An item of Data to be submitted to Graphite.

        @param name: Graphite data collection name
        @type  name: str

        @param time: Optional. Time value to submit data for in seconds since
                     Epoch. Default: time.time()
        @type  time: int

        @param value: Data value to be submitted.
        @type  value: str/int
    """
    import time as _time

    def __init__(self, name = None, time = int(_time.time()), value = None):
        self.name = name
        self.time = time
        self.value = value

    def __str__(self):
        # Return a string when a Datapoint is sent to 'print'
        return 'Counter: %s\nTime:    %s\nValue:   %s' % \
            (sanitize_name(self.name), self.time, self.value)

    def get_dict(self):
        """
            Return the datapoint as a dictionary
        """
        return {'target': sanitize_name(self.name),
                'time': self.time,
                'value': self.value}

    def get_string(self):
        """
            Return the datapoint as a string formatted for submission to
            Graphite
        """
        return "%s %s %s\n" % (sanitize_name(self.name), self.time, self.value)


class DataRequest():
    """
        Class used to define request parameters for Graphite queries

        @param target: String or list of string representing the graphite data
                       point names to be requested.
        @type  target: str/list

        @param tfrom: Optional. Relative or absolute timestamp of first data
                      point to be requested.
        @type  tfrom: str

        @param tuntil: Optional. Relative or absolute timestamp of last data
                         point to be requested.
        @type  tuntil: str
    """
    def __init__(self, target, tfrom = None, tuntil = None):
        self.target = sanitize_name(target)
        self.tfrom = tfrom
        self.tuntil = tuntil

    def __str__(self):
        return 'target: %s\nfrom: %s\nuntil: %s' % \
            (sanitize_name(self.target), self.tfrom, self.tuntil)

    def get_dict(self):
        """
            Return the current DataRequest object as a dictionary used by
            urllib to generate a Graphite request
        """
        option_dict = {'target': sanitize_name(self.target)}
        if self.tfrom:
            option_dict['from'] = self.tfrom
        if self.tuntil:
            option_dict['until'] = self.tuntil

        return option_dict


#------------------------------------------------------------------------------
# Custom functionality
#------------------------------------------------------------------------------
class Server(object):
    """
        A server object to handle passing data into and out of Graphite

        @param address: Required. Graphite server address
        @type  address: str

        @param password: Optional. Password for authentication with Graphite
                         server. If username is specified, and password is
                         None, the user will be prompted to enter a password.
        @type  password: str

        @param port: Optional. Graphite server port number. Default: 2003
        @type  port: int

        @param timeout: Optional. Socket timeout value in seconds. Default: 30
        @type  timeout: int

        @param username: Username for authentication with Graphite server
        @type  username: str
    """
    def __init__(self, address, port = 2003, timeout = 30, username = None,
                 password = None):
        self.address = address
        self.port = port
        self.timeout = timeout
        self._socket = None
        self._username = username

        if username and not password:
            # A username has been specified, but no password. Prompt for one.
            import getpass as _getpass
            self._password = _getpass.getpass('Password for %s: ' %
                                              (self._username))
        else:
            # A password has been specified.
            self._password = password

    def __str__(self):
        # Return a string when a Server is sent to 'print'
        return 'Address: %s\nPort: %s\nUsername: %s' % \
            (self.address, self.port, self._username)

    def _get_data(self, request):
        """
            Hidden function to handle the raw data retrieval from Graphite

            @param request: Dictionary of request options to send to Graphite
            @type  request: dict
        """
        import urllib as _urllib
        import urllib2 as _urllib2

        # Specify the http method to use to connect to the Graphite server
        requestmethod = 'https'
        # Build the base URL for the Graphite request
        requesturl = requestmethod + '://' + self.address + '/render'
        # Make sure our format option is valid
        if not request['format'].lower() in ['csv', 'json', 'xml']:
            request['format'] = 'raw'
        # Convert the dictionary of request options into a URL string.
        requestoptions = _urllib.urlencode(request, doseq = True)

        # Build a password manager for Graphite requests
        requestpassman = _urllib2.HTTPPasswordMgrWithDefaultRealm()
        # Add the specified username and password to the manager
        requestpassman.add_password(None, requesturl, self._username,
                                    self._password)

        # Create an authorization handler using our password manager
        requestauthhandler = _urllib2.HTTPBasicAuthHandler(requestpassman)

        # Create a URL Opener that uses our authorization handler
        requestopener = _urllib2.build_opener(requestauthhandler)

        # Install our URL opener so all urllib2.urlopen calls use it by default
        _urllib2.install_opener(requestopener)

        try:
            # Call our custom opener with the base URL and the URL options
            requesthandle = _urllib2.urlopen(requesturl, data = requestoptions)

            if not requesthandle.code == 200:
                # We didn't receive an exception, but the code is not an OK
                raise ConnectionError('Graphite server returned non-ok status:'
                                      ' %s' % (requesthandle.code))
            else:
                return requesthandle.read()
        except _urllib2.HTTPError, exc:
            raise ConnectionError('An error occurred requesting data from '
                                  'Graphite: %s: %s' % (exc.code, exc.msg))
        except _urllib2.URLError, exc:
            raise ConnectionError('An error occurred requesting data from  '
                                  'Graphite: %s' % (exc.reason))
        except Exception, exc:
            raise ConnectionError('Could not retrieve data from Graphite  '
                                  'server: %s' % (exc.message))

    def _send_data(self, data):
        """
            Send the contents of a single DataPoint to a Graphite server

            @param data: DataPoint object containing Graphite data to submit
            @type  data: DataPoint
        """
        if not self._socket:
            # The user hasn't connected yet. Do that form them.
            self.connect()

        # Call the datapoint's method to convert it into a string that is
        # understood by Graphite
        datastring = data.get_string()

        try:
            # Submit the datapoint's text to the Graphite socket
            # We use sendall() so an exception is raised if not all data has
            # been transmitted
            # successfully to the server.
            self._socket.sendall(datastring)
        except Exception, exc:
            # Catch-all exception to handle all possible socket errors
            raise ConnectionError('Could not transmit data to Graphite ' + \
                                  'server: %s' % (exc.strerr))

    def close(self):
        """
            Close the connection to the Graphite server
        """
        import socket as _serversocket

        if not self._socket:
            raise ConnectionError('Socket does not exist!')

        try:
            self._socket.shutdown(_serversocket.SHUT_RDWR)
            self._socket.close()
            self._socket = None
        except Exception, exc:
            raise ConnectionError('Error closing connection to the Graphite '
                                  'server: %s' % (exc.message))

    def connect(self):
        """
            Connect to the Graphite server
        """
        import socket as _serversocket

        if not self.address:
            # A server address hasn't been specified!
            raise ConnectionError('You must specify a Graphite server address'
                                  ' before establishing a connection')

        try:
            self._socket = _serversocket.socket(_serversocket.AF_INET,
                                                _serversocket.SOCK_STREAM)
            self._socket.settimeout(self.timeout)
            self._socket.connect((self.address, self.port))
        except _serversocket.timeout, exc:
            raise ConnectionError('The socket timed out while connecting to '
                                  'the Graphite server')
        except _serversocket.gaierror, exc:
            raise ConnectionError('A gai error occurred: %s' %
                                  (exc.strerror))
        except _serversocket.herror, exc:
            raise ConnectionError('A socket error occurred: %s' %
                                  (exc.strerror))
        except _serversocket.error, exc:
            raise ConnectionError('A socket error occurred: %s' %
                                  (exc.strerror))
        except Exception, exc:
            raise ConnectionError('Could not connect to the Graphite server'
                                  ' %s' % (exc.message))

    def get_csv(self, request):
        """
            Read data from Graphite server in CSV format

            @param request: DataRequest object containing Graphite query
                            options
            @type  request: DataRequest
        """
        import csv as _csv

        try:
            reqdict = request.get_dict()
            reqdict['format'] = 'csv'
            rawdata = self._get_data(reqdict)
            csvdata = _csv.reader(rawdata.split('\r\n'))
            return csvdata
        except ConnectionError:
            raise
        except Exception, exc:
            raise DataFormatError('Could not parse Graphite output to CSV:'
                                  ' %s' % (exc.message))

    def get_dplist(self, request):
        """
            Read data from Graphite server as a list of DataPoint() objects

            @param request: DataRequest object containing Graphite query
                            options
            @type  request: DataRequest
        """
        import sys

        try:
            # Initialize data variables for scope
            jsondata = None
            csvdata = None

            if sys.version_info < (2, 6):
                # This is python vertion 2.5.x or less
                csvdata = self.get_csv(request)
            else:
                # This is python version 2.6 or greater
                jsondata = self.get_json(request)

            # Create an empty list object
            dplist = []

            if jsondata:
                try:
                    # Iterate through each dictionary item in the JSON data
                    for jsonitem in jsondata:
                        # Make sure there's a valid target name. Verifying this is not
                        # an empty list item.
                        if 'target' in jsonitem.keys():
                            # Iterate through the datapoints listed for the target
                            for dataitem in jsonitem['datapoints']:
                                # Create a new DataPoint object and assign the proper
                                # values from the list
                                datapoint = DataPoint(name = jsonitem['target'],
                                                      time = dataitem[1],
                                                      value = dataitem[0])
                                # Append the DataPoint to the list of DataPoints
                                dplist.append(datapoint)
                except ConnectionError:
                    raise
                except DataFormatException:
                    raise
                except Exception, exc:
                    raise DataFormatError('Could not parse Graphite output to'
                                          ' JSON: %s' % (exc.message))
            elif csvdata:
                try:
                    # We need to convert the string time from graphite to an
                    # epoch/UNIX time
                    import calendar
                    import time

                    # Iterate through each dictionary item in the JSON data
                    for csvitem in csvdata:
                        if len(csvitem) is 3:
                            if csvitem[2] is '':
                                # Convert blank items into None
                                csvitem[2] = None

                            if not csvitem[1] is '':
                                # Convert the string date into unix time
                                csvitem[1] = calendar.timegm(
                                                         time.strptime(csvitem[1],
                                                         '%Y-%m-%d %H:%M:%S'))

                            # Build a DataPoint object with the correct values
                            datapoint = DataPoint(name = csvitem[0],
                                                  time = csvitem[1],
                                                  value = csvitem[2])
                            dplist.append(datapoint)
                except ConnectionError:
                    raise
                except DataFormatException:
                    raise
                except Exception, exc:
                    raise DataFormatError('Could not parse Graphite output to'
                                          ' JSON: %s' % (exc.message))

            # Return the list of DataPoint objects
            return dplist
        except ConnectionError:
            raise
        except Exception, exc:
            raise DataFormatError('Could not parse Graphite output:'
                                  ' %s' % (exc.message))

    def get_raw(self, request):
        """
            Read data from Graphite server in RAW format

            @param request: DataRequest object containing Graphite query
                            options
            @type  request: DataRequest
        """
        try:
            reqdict = request.get_dict()
            reqdict['format'] = 'raw'
            rawdata = self._get_data(reqdict)
            return rawdata
        except ConnectionError:
            raise
        except Exception, exc:
            raise DataFormatError('Could not parse Graphite output:'
                                  ' %s' % (exc.message))

    def get_json(self, request):
        """
            Read data from Graphite server in JSON format

            @param request: DataRequest object containing Graphite query
                            options
            @type  request: DataRequest
        """
        import sys

        # Make sure we have access to the json module.
        if sys.version_info < (2, 6):
            raise DataFormatError('This version of python is far out of date'
                                  ' and does not have a JSON module to parse'
                                  ' graphite output with. Please update to'
                                  ' python 2.6 or higher.')

        import json as _json

        try:
            reqdict = request.get_dict()
            reqdict['format'] = 'json'
            rawdata = self._get_data(reqdict)
            jsondata = _json.loads(rawdata)
            return jsondata
        except ConnectionError, exc:
            raise
        except Exception, exc:
            raise DataFormatError('Could not parse Graphite output to JSON:'
                                  ' %s' % (exc.message))

    def submit(self, data):
        """
            Submit a single DataPoint or a list of DataPoint to the Graphite
            server

            @param data: DataPoint or list of DataPoint object to submit
            @type  data: DataPoint or list
        """
        try:
            if not isinstance(data, list):
                data = [data]

            for dataitem in data:
                if isinstance(dataitem, DataPoint):
                    self._send_data(dataitem)
                else:
                    raise DataFormatError('You must provide a DataPoint to be '
                                          'submitted')
        except DataFormatError:
            # We raise this inside our try block, so pass it up the stack!
            raise
        except ConnectionError:
            # Re-raise connection errors raised in lower-level modules
            raise
        except Exception, exc:
            # Raise any un-handled lower-level exceptions
            raise ConnectionError('Could not submit data to Graphite server:'
                                  ' %s' % (exc.message))


def sanitize_name(name):
    """
        Convert the specified name to a Graphite-acceptable name

        @param name: String to make safe for graphite
        @type  name: str

        @return: Safe graphite name
        @type: str
    """
    import re as _re

    # Confirm we've received a string.
    if not (isinstance(name, str) or isinstance(name, unicode)):
        # name does not contain a string. Raise the proper error.
        raise DataFormatError('\'name\' must be a string')

    # Convert string to lower-case
    returnname = name.lower()
    # Replace any character that isn't a word, digit, or '.'
    repattern = _re.compile('[^\w^\d^\.]+')
    # Substitute the pattern matches with '_'
    returnname = repattern.sub('_', returnname)
    # Collapse duplicate '.'
    returnname = _re.sub('\.+', '.', returnname)
    # Collapse duplicate '_'
    returnname = _re.sub('_+', '_', returnname)
    # Trim leading and trailing '_'
    returnname = _re.sub('^_|_$', '', returnname)

    return str(returnname)

if __name__ == '__main__':
    print 'No tests defined'
