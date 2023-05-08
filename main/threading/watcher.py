"""
Watcher Worker that monitors the WorkerManager and stops it when all workers are stopped.
Author: Benjamin Dodd (1901386)
"""
import time
from main.threading import LOGGER
from main.threading.worker_thread import Worker

class WorkerManagerWatcher(Worker):
    """
    Worker thread that watches the worker threads.
    """

    def __init__(self, manager):
        super().__init__()
        self.manager = manager

    def work(self):
        while not self.is_stopped():
            LOGGER.debug("WorkerManager: thread count: %s", len(self.manager))
            time.sleep(3)