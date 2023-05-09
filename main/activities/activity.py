"""
Base class for all activities.
Author: Benjamin Dodd (1901386)
"""

import cv2 as cv

from main.activities import LOGGER

from main.threading.worker_manager import WorkerManager
from main.threading.worker_thread import Worker

class Activity(Worker):
    """
    Base class for all activities.
    """
    def __init__(self, name: str):
        super().__init__()
        self.name = name
        self.image = None

    def __str__(self):
        return f"Activity({self.name})"

    def __repr__(self):
        return self.__str__()
