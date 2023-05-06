"""
Manager class for the worker threads.
Author: Benjamin Dodd (1901386)
"""

import time
from typing import List
from atexit import register
from threading import Lock

from main.threading import LOGGER

from main.threading.worker_thread import WorkerThread
from main.threading.watcher import WorkerManagerWatcher

class WorkerManager:
    """
    Manager class for the worker threads.
    """

    _instance = None
    _instance_lock = Lock()
    _intitialized = False

    def __new__(cls, debug: bool = False):
        if cls._instance is None:
            with cls._instance_lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, debug: bool = False):
        if not self._intitialized:
            self.__workers: List[WorkerThread] = []
            register(self.stop_all_workers)
            self.debug = debug
            if debug:
                self.watcher = self.WorkerManagerWatcher(self)
                self.watcher.start()
            self._intitialized = True

    def __len__(self):
        return len(self.__workers)

    def add_worker(self, worker: WorkerThread):
        """Adds a WorkerThread to the manager.
        """
        if worker in self.__workers:
            raise ValueError("Worker already added")
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
        if self.debug:
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
