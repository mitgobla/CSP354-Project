import time
import unittest

from main.threading.worker_thread import WorkerThread
from main.threading.worker_manager import WORKER_MANAGER

class TestWorkerManager(unittest.TestCase):

    class TestThread(WorkerThread):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.count = 0

        def work(self):
            while not self.is_stopped():
                self.count += 1
                time.sleep(0.5)

    def test_all_stopped(self):
        threads = [TestWorkerManager.TestThread() for _ in range(5)]
        for thread in threads:
            WORKER_MANAGER.add_thread(thread)
        time.sleep(5)
        WORKER_MANAGER.stop_threads()
        self.assertTrue(WORKER_MANAGER.is_stopped())
