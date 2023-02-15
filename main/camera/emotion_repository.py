"""
A repository that stores the last emotion detected by the camera.
Author: Benjamin Dodd (1901386)
"""

import threading
import time

from . import LOGGER

from ..util.singleton import Singleton

UPDATE_INTERVAL = 1

class EmotionRepository(Singleton):

    __lock = threading.Lock()
    __current_emotion = None
    __last_update = 0

    @property
    def current_emotion(self):
        with self.__lock:
            return self.__current_emotion

    @current_emotion.setter
    def current_emotion(self, value):
        with self.__lock:
            # Check if the last update was more than UPDATE_INTERVAL seconds ago
            if time.time() - self.__last_update > UPDATE_INTERVAL:
                self.__last_update = time.time()
                self.__current_emotion = value
                LOGGER.debug("Current emotion: %s", value)

EMOTION_REPOSITORY = EmotionRepository()
