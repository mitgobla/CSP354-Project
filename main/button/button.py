"""
Driver class for a button.
Author: Benjamin Dodd (1901386)
"""

import threading
import time

from . import LOGGER
from .button_repository import BUTTON_REPOSITORY

try:
    import RPi.GPIO as GPIO
except ImportError:
    from ..util.mock_gpio import MockGPIO as GPIO

from ..util.singleton import Singleton

class Button(metaclass = Singleton):
    """
    Driver class for a button.
    """

    def __init__(self, pin: int):
        """Create a new instance of the Button class."""
        self.pin = pin
        self.setup()

        self._state_thread = threading.Thread(target = self.state_thread)
        self._state_thread.start()

    def setup(self):
        """
        Set up the GPIO pins for the button.
        """
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)

    def state_thread(self):
        """
        Updates the button state in the repository.
        """
        while True:
            state = self.is_pressed()
            if BUTTON_REPOSITORY.button_state != state:
                BUTTON_REPOSITORY.button_state = state
            time.sleep(1.0)

    def is_pressed(self) -> bool:
        """
        Check if the button is pressed.
        """
        state = GPIO.input(self.pin) == GPIO.LOW
        return state


BUTTON = Button(7)

if __name__ == "__main__":
    while True:
        time.sleep(0.1)
