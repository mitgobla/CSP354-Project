import time
import unittest

from main.threading.worker_thread import Worker
from main.threading.worker_manager import WorkerManager

class TestWorkerThread(unittest.TestCase):

    worker_manager = WorkerManager()

    def __init__(self, methodName: str = "runTest"):
        super().__init__(methodName)
        Worker.set_manager(self.worker_manager)
    class TestThread(Worker):
        def __init__(self):
            super().__init__()
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
        self.assertTrue(thread.count == 10, f"thread.count = {thread.count}")
