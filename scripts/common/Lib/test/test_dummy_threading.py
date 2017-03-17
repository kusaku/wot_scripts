# Embedded file name: scripts/common/Lib/test/test_dummy_threading.py
from test import test_support
import unittest
import dummy_threading as _threading
import time

class DummyThreadingTestCase(unittest.TestCase):

    class TestThread(_threading.Thread):

        def run(self):
            global running
            delay = 0
            if test_support.verbose:
                print 'task', self.name, 'will run for', delay, 'sec'
            sema.acquire()
            mutex.acquire()
            running += 1
            if test_support.verbose:
                print running, 'tasks are running'
            mutex.release()
            time.sleep(delay)
            if test_support.verbose:
                print 'task', self.name, 'done'
            mutex.acquire()
            running -= 1
            if test_support.verbose:
                print self.name, 'is finished.', running, 'tasks are running'
            mutex.release()
            sema.release()

    def setUp(self):
        global running
        global mutex
        global sema
        self.numtasks = 10
        sema = _threading.BoundedSemaphore(value=3)
        mutex = _threading.RLock()
        running = 0
        self.threads = []

    def test_tasks(self):
        for i in range(self.numtasks):
            t = self.TestThread(name='<thread %d>' % i)
            self.threads.append(t)
            t.start()

        if test_support.verbose:
            print 'waiting for all tasks to complete'
        for t in self.threads:
            t.join()

        if test_support.verbose:
            print 'all tasks done'


def test_main():
    test_support.run_unittest(DummyThreadingTestCase)


if __name__ == '__main__':
    test_main()