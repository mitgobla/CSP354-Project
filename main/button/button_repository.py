"""
A repository that stores the last button press.
Author: Benjamin Dodd (1901386)
"""

import threading

from . import LOGGER

from ..util.singleton import Singleton

class ButtonRepository(metaclass = Singleton):

    __lock = threading.Lock()
    __button_state = None

    @property
    def button_state(self):
        with self.__lock:
            return self.__button_state

    @button_state.setter
    def button_state(self, value):
        with self.__lock:
            self.__button_state = value
            LOGGER.debug("Button state: %s", value)

BUTTON_REPOSITORY = ButtonRepository()
