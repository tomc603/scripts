#!/usr/bin/env python

import threading
import Queue
import time

class Producer(threading.Thread):
    def __init__(self, in_queue, out_queue):
        threading.Thread.__init__(self)
        self.in_queue = in_queue
        self.out_queue = out_queue

    def run(self):
        # Max wait-time for the first queue item to appear
        qwait = 30
        ok = True

        while ok:
            try:
                item = self.in_queue.get(qwait)
                ok = True
                qwait = 0.5
                self.out_queue.put(item)
                self.in_queue.task_done()

            except:
                print 'Producer: Not OK'
                ok = False


class Consumer(threading.Thread):
    def __init__(self, out_queue):
        threading.Thread.__init__(self)
        self.out_queue = out_queue

    def run(self):
        while not out_queue.empty():
            item = self.out_queue.get()
            self.out_queue.task_done()


if __name__ == '__main__':
    threadcount = 1
    itemcount = 1000000
    in_queue = Queue.Queue()
    out_queue = Queue.Queue()

    fillstart = time.time()
    for item in xrange(itemcount):
        itemval = 'item-%d' % (item)
        in_queue.put(itemval)
    print 'ADD : %f items/sec.\n' % (itemcount / (time.time() - fillstart))

    movestart = time.time()
    while not in_queue.empty():
        item = in_queue.get(block = False)
        out_queue.put(item, block = False)
        in_queue.task_done()
    print 'MOVE: %f items/sec.\n' % (itemcount / (time.time() - movestart))

    getstart = time.time()
    while not out_queue.empty():
        item = out_queue.get(block = False)
        out_queue.task_done()
    print 'GET : %f items/sec.\n' % (itemcount / (time.time() - getstart))
