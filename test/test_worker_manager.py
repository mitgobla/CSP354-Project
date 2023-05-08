import time
import unittest

from main.threading.worker_thread import Worker
from main.threading.worker_manager import WorkerManager

class TestWorkerManager(unittest.TestCase):

    worker_manager = WorkerManager()

    class TestThread(Worker):
        def __init__(self, manager, *args, **kwargs):
            super().__init__(manager, *args, **kwargs)
            self.count = 0

        def work(self):
            while not self.is_stopped():
                self.count += 1
                time.sleep(0.5)

    def test_all_stopped(self):
        workers = [TestWorkerManager.TestThread(self.worker_manager) for _ in range(5)]
        for worker in workers:
            worker.start()
        time.sleep(5)
        self.worker_manager.stop_all_workers()
        self.assertTrue(self.worker_manager.is_stopped())
