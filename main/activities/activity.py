"""
Base class for all activities.
Author: Benjamin Dodd (1901386)
"""

from main.activities import LOGGER

from main.threading.worker_manager import WorkerManager
from main.threading.worker_thread import WorkerThread

class Activity(WorkerThread):
    """
    Base class for all activities.
    """
    def __init__(self, name: str, worker_manager: WorkerManager):
        super().__init__()
        self.name = name
        self.running = False
        self.worker_manager = worker_manager


    def __str__(self):
        return f"Activity({self.name})"

    def __repr__(self):
        return self.__str__()

    def start(self):
        """
        Starts the activity.
        """
        self.running = True
        self.worker_manager.add_worker(self)

    def stop(self):
        """
        Stops the activity.
        """
        self.running = False
