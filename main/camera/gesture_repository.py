"""
A repository that stores the last gesture detected by the camera.
Author: Benjamin Dodd (1901386)
"""

import threading

from ..util.singleton import Singleton

class GestureRepository(Singleton):

    __lock = threading.Lock()
    __current_gesture = None

    @property
    def current_gesture(self):
        with self.__lock:
            return self.__current_gesture

    @current_gesture.setter
    def current_gesture(self, value):
        with self.__lock:
            self.__current_gesture = value

GESTURE_REPOSITORY = GestureRepository()