"""
Manager class for the worker threads.
Author: Benjamin Dodd (1901386)
"""

from typing import List
from atexit import register

from . import LOGGER

from ..util.singleton import Singleton

from .worker_thread import WorkerThread

class WorkerManager(metaclass=Singleton):
    """
    Manager class for the worker threads.
    """

    def __init__(self):
        self.__threads: List[WorkerThread] = []
        register(self.stop_threads)

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
        self.__threads.remove(thread)

WORKER_MANAGER = WorkerManager()
