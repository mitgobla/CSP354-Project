"""
Manager class for the worker threads.
Author: Benjamin Dodd (1901386)
"""

from typing import List, Callable

from ..util.singleton import Singleton

from .worker_thread import WorkerThread

class WorkerManager(metaclass=Singleton):
    """
    Manager class for the worker threads.
    """

    def __init__(self):
        self.__threads: List[WorkerThread] = []

    def add_thread(self, worker: WorkerThread):
        """Adds a thread to the manager.

        Args:
            target (Callable): Function to run in the thread.
        """

        worker.start()
        self.__threads.append(worker)

    def stop_threads(self):
        """
        Stops all threads.
        """
        for thread in self.__threads:
            thread.stop()

    def restart_threads(self):
        """
        Restarts all threads.
        """
        for thread in self.__threads:
            thread.restart()

    def is_stopped(self):
        """Returns whether all threads are stopped.

        Returns:
            bool: True if all threads are stopped, False otherwise.
        """
        for thread in self.__threads:
            if not thread.is_stopped():
                return False
        return True

WORKER_MANAGER = WorkerManager()
