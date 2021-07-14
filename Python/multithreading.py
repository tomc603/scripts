#!/usr/bin/env python

import logging
import threading
import time
import Queue

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s',)


def wait_for_event_timeout(e, q):
    """
        Process items in queue 'q' until e.isSet() returns True or the queue
        is empty.
    """
    while not e.isSet() and not q.empty():
        try:
            logging.debug('e is not set')
            queueitem = q.get(False)
            logging.debug('queueitem: ' + str(queueitem))
            q.task_done()
        except Queue.Empty:
            logging.debug('Exception: Queue is empty. Ending.')


itemqueue = Queue.Queue()
for i in xrange(40000):
    itemqueue.put(i)

e = threading.Event()
for tc in xrange(5):
    t = threading.Thread(target=wait_for_event_timeout, args=(e, itemqueue))
    t.start()

while not itemqueue.empty():
    logging.debug('itemqueue is not empty')
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        logging.debug('Caught ctrl-c. Setting event.')
        e.set()
        logging.debug('e is set')
        waitcount = 0
        while len(threading.enumerate()) > 1 and waitcount < 30:
            logging.debug('Waiting for threads to die...' + str(len(threading.enumerate())))
            time.sleep(1)
            waitcount += 1
            logging.debug('Waitcount: ' + str(waitcount))
        break

#logging.debug('Queue looks empty. Setting event.')
#e.set()
#logging.debug('e is set')
logging.debug('Done.')
