import time
import unittest

from main.threading.worker_thread import WorkerThread

class TestWorkerThread(unittest.TestCase):

    class TestThread(WorkerThread):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.count = 0

        def work(self):
            while not self.is_stopped():
                self.count += 1
                time.sleep(0.5)

    def test_stop(self):
        thread = TestWorkerThread.TestThread()
        thread.start()
        time.sleep(5)
        thread.stop()
        self.assertTrue(thread.is_stopped())

    def test_value(self):
        thread = TestWorkerThread.TestThread()
        thread.start()
        time.sleep(5)
        thread.stop()
        self.assertTrue(thread.count == 10)
