"""
A repository that stores the last emotion detected by the camera.
Author: Benjamin Dodd (1901386)
"""

import threading

from ..util.singleton import Singleton

class EmotionRepository(Singleton):

    __lock = threading.Lock()
    __current_emotion = None

    @property
    def current_emotion(self):
        with self.__lock:
            return self.__current_emotion

    @current_emotion.setter
    def current_emotion(self, value):
        with self.__lock:
            self.__current_emotion = value

EMOTION_REPOSITORY = EmotionRepository()
