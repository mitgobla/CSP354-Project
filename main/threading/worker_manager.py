"""
Manager class for the worker threads.
Author: Benjamin Dodd (1901386)
"""

import time
from typing import List
from atexit import register

from . import LOGGER

from .worker_thread import WorkerThread

class WorkerManager:
    """
    Manager class for the worker threads.
    """
    class WorkerManagerWatcher(WorkerThread):
        """
        Worker thread that watches the worker threads.
        """

        def __init__(self, manager: "WorkerManager"):
            super().__init__()
            self.manager = manager

        def work(self):
            while not self.is_stopped():
                LOGGER.debug("WorkerManager: thread count: %s", len(self.manager))
                time.sleep(3)


    def __init__(self):
        self.__workers: List[WorkerThread] = []
        register(self.stop_all_workers)
        self.watcher = self.WorkerManagerWatcher(self)
        self.watcher.start()

    def __len__(self):
        return len(self.__workers)

    def add_worker(self, worker: WorkerThread):
        """Adds a WorkerThread to the manager.
        """
        worker.manager = self
        worker.start()
        self.__workers.append(worker)
        # LOGGER.debug("Worker added: %s", worker)

    def stop_all_workers(self):
        """
        Stops all workers.
        """
        for thread in self.__workers:
            thread.stop()
        self.watcher.stop()
        LOGGER.debug("All workers stopped")

    def is_stopped(self):
        """Returns whether all threads are stopped.

        Returns:
            bool: True if all threads are stopped, False otherwise.
        """
        for thread in self.__workers:
            if not thread.is_stopped():
                return False
        return True

    def remove_worker(self, thread: WorkerThread):
        """
        Removes a worker from the manager.

        Args:
            thread (WorkerThread): Worker to delete.
        """
        # LOGGER.debug("Removing worker: %s", thread)
        if thread in self.__workers:
            if not thread.is_stopped():
                thread.stop()
            self.__workers.remove(thread)
            # LOGGER.debug("Worker removed: %s", thread)

WORKER_MANAGER = WorkerManager()
