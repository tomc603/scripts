#!/usr/bin/python2.7

__author__ = 'tcameron'

'''
tbap - Touched By A Python

This utility creates files in a set of directories to exercise the
basic metadata operations of a filesystem.

A user specifies the number of directory levels to create, and the number of
directories to create at those levels. Finally, the specified number of
files is created in each directory.
'''

import argparse
import os

DODRY=False
VERBOSE=False

def makefiles(path, count):
    for i in xrange(0, count):
        fname = os.path.join(path, '%d.file' % i)
        try:
            if VERBOSE:
                print('FILE: %s' % fname)
            if not DODRY:
                f = open(fname, mode='w')
                f.close()
        except Exception as e:
            print('Could not create file %s: %s' % (fname, e))

def makedir(path):
    try:
        if VERBOSE:
            print('DIR : %s' % path)
        if not DODRY:
            os.mkdir(path)
    except Exception as e:
        print('Could not create directory %s: %s' % (path, e))

def makedirs(path, maxdepth, curdepth, maxwidth):
    # Create file entries in the current directory
    makefiles(path, maxwidth)

    # Create sub-directories for the width of the current directory
    for i in xrange(0, maxwidth):
        newpath = '%s/%i' % (path, i)
        makedir(newpath)

        # Create depth directories under each sub-directory
        if curdepth < maxdepth:
                makedirs(newpath, maxdepth, curdepth + 1, maxwidth)

def dotest(maxdepth, maxwidth, path):
    makedirs(path, maxdepth, 0, maxwidth)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--verbose', help='Increased output while running',
                    action='store_true')
    ap.add_argument('--dry', help='Perform a dry-run, not actually creating '
                                  'files or directories.',
                    action='store_true')
    ap.add_argument('--depth', help='Number of subdirectory levels to '
                                    'create', type=int)
    ap.add_argument('--width', help='Number of files and subdirectories to '
                                    'create under each depth directory',
                    type=int)
    ap.add_argument('--path', help='Top level path to execute test', type=str)
    args = ap.parse_args()

    VERBOSE = args.verbose
    DODRY = args.dry
    dotest(args.depth, args.width, args.path)
