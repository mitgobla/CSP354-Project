"""
Manager class for the worker threads.
Author: Benjamin Dodd (1901386)
"""

import time
from typing import List
from atexit import register

from . import LOGGER

from ..util.singleton import Singleton

from .worker_thread import WorkerThread

class WorkerManager(metaclass=Singleton):
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
        self.__threads: List[WorkerThread] = []
        register(self.stop_threads)
        self.watcher = self.WorkerManagerWatcher(self)
        self.watcher.start()

    def __len__(self):
        return len(self.__threads)

    def add_thread(self, worker: WorkerThread):
        """Adds a WorkerThread to the manager.
        """
        worker.manager = self
        worker.start()
        self.__threads.append(worker)

    def stop_threads(self):
        """
        Stops all threads.
        """
        for thread in self.__threads:
            thread.stop()
        self.watcher.stop()

    def is_stopped(self):
        """Returns whether all threads are stopped.

        Returns:
            bool: True if all threads are stopped, False otherwise.
        """
        for thread in self.__threads:
            if not thread.is_stopped():
                return False
        return True

    def delete_thread(self, thread: WorkerThread):
        """
        Deletes a thread from the manager.

        Args:
            thread (WorkerThread): Thread to delete.
        """
        if thread in self.__threads:
            if not thread.is_stopped():
                thread.stop()
            self.__threads.remove(thread)

WORKER_MANAGER = WorkerManager()
