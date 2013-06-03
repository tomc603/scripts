#!/usr/bin/env python
import os
import random
import threading
import time


class threadsafe_iter():
    """Takes an iterator/generator and makes it thread-safe by
    serializing call to the `next` method of given iterator/generator.
    """
    def __init__(self, it):
        self.it = it
        self.lock = threading.Lock()

    def __iter__(self):
        return self

    def next(self):
        with self.lock:
            return self.it.next()


class SpoolDir(object):
    def __init__(self, spooldir, spooldepth = 2, spoolwidth = 100):
        self.spooldir = spooldir
        self.spooldepth = spooldepth
        self.spoolwidth = spoolwidth
        self.initialized = False

    def __mkDirs(self, path, depth, width):
        '''
        Create a list of zero-padded directories from 00 to width,
        and repeat the process under each created directory for a maximum
        number of depth times.
        This gives a fanned out width ^ depth structure,
        which should provide an adequate directory heirarchy to choose
        random directories from when creating spool files.

        :param path: Directory to create subdirectories in
        :type path: str
        :param depth: Maximum level of recursion into subdirectories
        :type depth: int
        :param width: Maximum number of directories to create in the current
         path
        :type width: int
        '''
        for a in xrange(width):
            # Join a zero-padded directory name to the specified path
            curpath = os.path.join(path, '%.2d' % a)

            # If the directory does not exist, create it.
            if not os.path.exists(curpath):
                os.mkdir(curpath, 0770)

            # Continue creating directories if we haven't reached out max
            # depth
            if depth -1 > 0:
                self.__mkDirs(curpath, (depth - 1), width)

    def __rmDirs(self, path, keepCurDir=False):
        '''
        Depth-first cleanup of a spool directory. Traverse a directory
        structure, passing any directory we find to a new call to this
        function. If we find a non-directory item, we delete it.

        :param path: Current directory in the tree
        :type path: str
        '''

        # If the current path is a directory...
        if os.path.isdir(path):
            # Loop through the contents of the directory
            for spooldata in os.listdir(path):
                newpath = os.path.join(path, spooldata)

                if os.path.isdir(newpath):
                    # The current item is a directory,
                    # call __rmDir() with the current item as the path.
                    self.__rmDirs(newpath)
                else:
                    # The current item is a file. Delete it.
                    os.remove(newpath)

            if not keepCurDir:
                # Finally, delete the current directory
                os.rmdir(path)

    def __getDir(self, path):
        '''
        Return a spool directory from the deepest level. Each level will
         be randomized and passed to a re-entrant call to this function
         until there are no more directories in the depth search.

        :param path: Current directory in the tree
        :type path: str
        :return: Randomly chosen directory
        :rtype: str
        '''

        # If the current path is a directory...
        if os.path.isdir(path):
            # Collect a list of only subdirectories
            subdirlist = filter(os.path.isdir, [os.path.join(path, x) for
                                                x in os.listdir(path)])

            # If one or more subdirectories were found...
            if subdirlist:
                # Randomly choose a subdirectory
                newpath = os.path.join(path, random.choice(subdirlist))

                # Call this function with the subdirectory joined to the
                #  current path
                subpath = self.__getDir(newpath)

                if subpath:
                    return subpath
                else:
                    return newpath
            else:
                return path

    def threadsafe_generator(f):
        """A decorator that takes a generator function and makes it thread-safe.
        """
        def g(*a, **kw):
            return threadsafe_iter(f(*a, **kw))
        return g

    def mkSpoolDir(self):
        spooldir_start = time.time()

        # Create the top-level directory if it doesn't exist
        if not os.path.exists(self.spooldir):
            os.mkdir(self.spooldir, 0770)

        # Call the recursive __mkDirs() to actually build a fanned-out spool
        #  directory structure.
        self.__mkDirs(self.spooldir, self.spooldepth, self.spoolwidth)

        # Set the initialized flag
        self.initialized = True

        # Report the total time spent creating directories.
        print('mkSpoolDir time: %f' % (time.time() - spooldir_start))

    def delSpoolDir(self, delTopDir=False):
        delete_start = time.time()

        # If the specified directory exists, call the re-entrant worker
        # function to actually delete its contents depth-first.
        if os.path.exists(self.spooldir):
            self.__rmDirs(self.spooldir, not delTopDir)

        # Reset the initialized flag to prevent usage of a non-existent
        # directory structure.
        self.initialized = False

        # Output the total time spent deleting directories
        print('delSpoolDir time: %f' % (time.time() - delete_start))

    @threadsafe_generator
    def getSpoolFile(self):
        if not self.initialized:
            raise StopIteration('Spool directory is not initialized!')

        while True:
            if os.path.exists(self.spooldir):
                chosenpath = self.__getDir(self.spooldir)
                yield os.path.join(chosenpath, '%.3f' % time.time())


class SpoolWriter(threading.Thread):
    def __init__(self, threadname, spooldirobj, filecount, filedata):
        threading.Thread.__init__(self)
        self.threadname = threadname
        self.spooldirobj = spooldirobj
        self.filecount = filecount
        self.filedata = filedata

    def run(self):
        loc = threading.local()
        loc.writestart = time.time()

        print('%s: Writing %d spool files' % (self.threadname,
                                              self.filecount))
        for i in xrange(self.filecount):
            spoolfile = self.spooldirobj.next()
            with open(spoolfile, 'w') as loc.sf:
                loc.sf.write(self.filedata)
                loc.sf.flush()
                os.fsync(loc.sf)
        loc.writeend = time.time()
        print('%s: Done - %f sec. -> %f files/sec' %
              (self.threadname, loc.writeend - loc.writestart,
               self.filecount / (loc.writeend - loc.writestart)))


def spoolTester(spoolpath):
    # Mark what time we start
    test_start_time = time.time()

    # Initialize a SpoolDir object
    sd = SpoolDir(spoolpath)

    # Initialize and build the spool dir
    sd.mkSpoolDir()

    # Get a file path generator object
    spoolfiles = sd.getSpoolFile()

    spoolcount = 10000
    spoolchars = 'abcde' * 10000

    threadcount = 8
    threadlist = []
    for i in xrange(threadcount):
        threadlist.append(SpoolWriter('Thread-%.2d' % i, spoolfiles,
                                      spoolcount/threadcount, spoolchars))

    for t in threadlist:
        t.start()

    for t in threadlist:
        t.join()

    # Clean up the spool directory
    #sd.delSpoolDir()

    # Note how long the total run time was
    print('Total runtime: %f' % (time.time() - test_start_time))


if __name__ == '__main__':
    spoolTester('/home/tcameron/tmp/spool')
