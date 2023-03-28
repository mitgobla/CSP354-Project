"""
A repository that stores the last button press.
Author: Benjamin Dodd (1901386)
"""

from threading import Lock
from . import LOGGER

class ButtonRepository():

    _instance_lock = Lock()
    _instance = None

    _button_state_lock = Lock()
    _button_state = False

    def __new__(cls):
        if cls._instance is None:
            with cls._instance_lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    @property
    def button_state(self):
        with self._button_state_lock:
            return self._button_state

    @button_state.setter
    def button_state(self, value):
        with self._button_state_lock:
            self._button_state = value
            LOGGER.debug("Button state: %s", value)

BUTTON_REPOSITORY = ButtonRepository()
