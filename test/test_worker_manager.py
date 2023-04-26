import time
import unittest

from main.threading.worker_thread import WorkerThread
from main.threading.worker_manager import WorkerManager

class TestWorkerManager(unittest.TestCase):

    worker_manager = WorkerManager()

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
            self.worker_manager.add_worker(thread)
        time.sleep(5)
        self.worker_manager.stop_all_workers()
        self.assertTrue(self.worker_manager.is_stopped())
