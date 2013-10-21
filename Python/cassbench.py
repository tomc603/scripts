__author__ = 'tcameron'

from cqlengine import columns
from cqlengine.models import Model
from cqlengine import connection
import logging
import multiprocessing
from Queue import Queue, Empty, Full
from sys import stderr
from time import sleep


# Define "global" variables
MAXPROCS = 4


class QLDEntry(Model):
    first_name = columns.Text(primary_key=True)
    last_name = columns.Text()


def enqueue(l, c, q):
    plist = []
    l.debug('Spawning enqueue processes')
    for i in xrange(MAXPROCS):
        p = multiprocessing.Process(target=EnqueuePeople, args=(l, c, q,),
                                    name='EeQueue-%d' % i)
        plist.append(p)
        # t.daemon = True
        p.start()
        p.join()
    l.debug('Done spawning enqueue processes')
    l.debug('plist: %r' % plist)

    while len(multiprocessing.active_children()) > 0:
        l.debug('Waiting for %d enqueue processes'
                % len(multiprocessing.active_children()))
        try:
            l.info('Queue: %d items.' % q.qsize())
            l.debug('plist: %r' % plist)
            sleep(1)
        except KeyboardInterrupt:
            l.critical('Caught ctrl-c. Stopping worker processes.')
            for p in multiprocessing.active_children():
                p.terminate()
            while len(multiprocessing.active_children()) > 0:
                l.info('Waiting for %d remaining processes to die.'
                       % len(multiprocessing.active_children()))
                sleep(1)
            break
    l.debug('Done waiting for enqueue processes')


def dequeue(l, q):
    l.debug('Spawning dequeue processes')
    for i in xrange(MAXPROCS):
        p = multiprocessing.Process(target=DequeuePeople, args=(l, q,),
                                    name='DeQueue-%d' % i)
        p.daemon = True
        p.start()
    l.debug('Done spawning dequeue processes')

    l.debug('Waiting for dequeue processes')
    while len(multiprocessing.active_children()) > 0:
        try:
            sleep(1)
            l.info('Queue: %d items.' % q.qsize())
        except KeyboardInterrupt:
            l.critical('Caught ctrl-c. Stopping worker processes.')
            for p in multiprocessing.active_children():
                p.terminate()
            while len(multiprocessing.active_children()) > 0:
                l.info('Waiting for %d remaining processes to die.'
                       % len(multiprocessing.active_children()))
                sleep(1)
            break
    l.debug('Done waiting for dequeue processes')


def EnqueuePeople(l, count, q):
    l.debug('Start EnqueuePeople()')
    for i in xrange(count):
        q.put(QLDEntry(first_name='Tom %d' % i, last_name='%d Cameron' % i),
              block=True, timeout=2)
    l.debug('End EnqueuePeople()')


def DequeuePeople(l, q):
    l.debug('Start DequeuePeople()')
    while not q.empty():
        p = q.get(True, 1)
    l.debug('End DequeuePeople()')


def main():
    """
    Define script parameters
    """
    LOGLEVEL = logging.DEBUG
    ITEMCOUNT = 100000

    # Set up logging
    logformatter = logging.Formatter('%(asctime)s - %(process)d'
                                     ' - %(levelname)s - %(message)s')

    loghandler = logging.StreamHandler(stderr)
    loghandler.setFormatter(logformatter)
    loghandler.setLevel(LOGLEVEL)

    scriptlogger = logging.getLogger('cassbench')
    scriptlogger.addHandler(loghandler)
    scriptlogger.setLevel(LOGLEVEL)
    scriptlogger.debug('Script logging enabled')

    # Set up variables needed by processes
    iq = Queue()

    # Call function to create, start, and wait for enqueue processes
    # enqueue(scriptlogger, ITEMCOUNT, iq)

    plist = []
    scriptlogger.debug('Spawning enqueue processes')
    for i in xrange(MAXPROCS):
        p = multiprocessing.Process(target=EnqueuePeople, args=(scriptlogger,
                                                                ITEMCOUNT,
                                                                iq,),
                                    name='EeQueue-%d' % i)
        # t.daemon = True
        p.start()
    scriptlogger.debug('Done spawning enqueue processes')

    while len(multiprocessing.active_children()) > 0:
        scriptlogger.debug('Waiting for %d enqueue processes'
                           % len(multiprocessing.active_children()))
        try:
            scriptlogger.info('Queue: %d items.' % iq.qsize())
            sleep(1)
        except KeyboardInterrupt:
            scriptlogger.critical('Caught ctrl-c. Stopping worker processes.')
            for p in multiprocessing.active_children():
                p.terminate()
            while len(multiprocessing.active_children()) > 0:
                scriptlogger.info('Waiting for %d remaining processes to die.'
                                  % len(multiprocessing.active_children()))
                sleep(1)
            break
    scriptlogger.debug('Done waiting for enqueue processes')

    # Call function to create, start, and wait for dequeue processes
    dequeue(scriptlogger, iq)
    scriptlogger.info('Queue: %d items.' % iq.qsize())

if __name__ == "__main__":
    main()
