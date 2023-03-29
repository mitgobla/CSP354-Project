"""
A repository that stores the last button press.
Author: Benjamin Dodd (1901386)
"""

from threading import Lock
from .button import Button

class ButtonRepository():

    _instance_lock = Lock()
    _instance = None

    _button_state_lock = Lock()
    _button_states = {}

    def __new__(cls):
        if cls._instance is None:
            with cls._instance_lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def update_button_state(self, button: Button, state: bool):
        """
        Update the state of a button.
        """
        with self._button_state_lock:
            self._button_states[button] = state

    def get_button_state(self, button: Button):
        """
        Get the state of a button.
        """
        with self._button_state_lock:
            return self._button_states.get(button, False)

    def has_button(self, button: Button):
        """
        Check if a button is in the repository.
        """
        with self._button_state_lock:
            return button in self._button_states
