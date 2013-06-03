#!/usr/bin/env python

import os
import sys
import re
import glob


def showusage():
    print('Usage: %s sourcedir destfile' % (sys.argv[0]))

# Regexes to find the lines we want
re_threads = re.compile('results: Threads: .*')
re_sent = re.compile('results: Sent: .*')
re_received = re.compile('results: Received: .*')
re_rxqps = re.compile('results: Received_QPS: .*')
re_txqps = re.compile('results: Target_QPS: .*')

# Check argument count
if '--help' in sys.argv or '-h' in sys.argv:
    # User requested help on the CLI
    showusage()

    # Return a good exit code to the shell
    sys.exit(0)

if not len(sys.argv) == 3:
    # User did not specify the correct number of parameters
    # and did not request help.
    print('ERROR: You must enter a source and destination.')
    showusage()

    # Return a parameter error value to the shell
    sys.exit(1)

if not os.path.isdir(sys.argv[1]):
    print('ERROR: The source directory specified is not a directory or does not exist.')
    showusage()

    # Return a parameter error value to the shell
    sys.exit(1)

try:
    print('Generating %s' % sys.argv[2])

    # Open the output file
    outfile = open(sys.argv[2], 'w')

    # Print the CSV header line
    outfile.writelines('OS,Threads,IPs,Ports,Target_QPS,Sent,Received,Received_QPS\n')

    # Loop through the result files in the current working directory
    for statsfile in os.listdir(sys.argv[1]):
        if not os.path.isfile(os.path.join(sys.argv[1], statsfile)):
            # Skip directories and other items that are not a file.
            continue

        try:
            # Initialize the sent and received values to something sane for a CSV
            threads = "0"
            sentcount = "0"
            receivedcount = "0"
            rxqps = "0"
            txqps = 0

            # Read result type information from the file name.
            splitname = statsfile.split('.')

            platform = splitname[4]
            ipcount = splitname[1]
            ports = splitname[2]

            infile = open(os.path.join(sys.argv[1], statsfile), 'r')
            fdata = infile.read()

            # Select the sent and received values from the result file
            threads = re_threads.findall(fdata)[0].split()[-1]
            sentcount = re_sent.findall(fdata)[0].split()[-1]
            receivedcount = re_received.findall(fdata)[0].split()[-1]
            rxqps = re_rxqps.findall(fdata)[0].split()[-1]
            txqps = re_txqps.findall(fdata)[0].split()[-1]

            # Only print lines that do not contain errors.
            outfile.writelines('%s,%s,%s,%s,%s,%s,%s,%s\n' %
                               (platform, threads, ipcount, ports, txqps,
                                sentcount, receivedcount, rxqps))

        except IndexError:
            print('ERROR: Malformed data: %s' % statsfile)
            continue

        except IOError:
            print('ERROR: Could not read stats file %s. Skipping.' % statsfile)
            continue

        except:
            # Skip this line or file. It has an error.
            # print 'Error reading file %s' % (file)
            continue

        finally:
            # Be kind and close the result file
            infile.close()
            outfile.flush()

    # Return a good exit code to the shell
    sys.exit(0)
except IOError:
    print('ERROR: Could not open output file')
    showusage()

    # Return a file error value to the shell
    sys.exit(2)
