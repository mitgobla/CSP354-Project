"""
A repository that stores the last gesture detected by the camera.
Author: Benjamin Dodd (1901386)
"""

import threading

from . import LOGGER

from ..util.singleton import Singleton

class GestureRepository(metaclass = Singleton):

    __lock = threading.Lock()
    __current_gesture = None

    @property
    def current_gesture(self):
        with self.__lock:
            return self.__current_gesture

    @current_gesture.setter
    def current_gesture(self, value):
        with self.__lock:
            LOGGER.debug("GestureRepository: Setting current gesture to %s", value)
            self.__current_gesture = value

GESTURE_REPOSITORY = GestureRepository()
