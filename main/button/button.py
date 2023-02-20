"""
Driver class for a button.
Author: Benjamin Dodd (1901386)
"""

import time

from . import LOGGER
from .button_repository import BUTTON_REPOSITORY

try:
    import RPi.GPIO as GPIO
except ImportError:
    from ..util.mock_gpio import MockGPIO as GPIO

from ..threading.worker_manager import WORKER_MANAGER
from ..threading.worker_thread import WorkerThread
from ..util.singleton import Singleton

class Button(metaclass = Singleton):
    """
    Driver class for a button.
    """

    class ButtonWorker(WorkerThread):
        """
        Worker thread for the button.
        """

        def __init__(self, button: "Button"):
            """Create a new instance of the ButtonWorker class."""
            super().__init__()
            self.button = button

        def work(self):
            """
            Run the worker thread.
            """
            while not self.is_stopped():
                state = self.button.is_pressed()
                if BUTTON_REPOSITORY.button_state != state:
                    BUTTON_REPOSITORY.button_state = state
                time.sleep(0.1)

    def __init__(self, pin: int):
        """Create a new instance of the Button class."""
        self.pin = pin
        self.setup()

        self.worker = self.ButtonWorker(self)
        WORKER_MANAGER.add_thread(self.worker)

    def setup(self):
        """
        Set up the GPIO pins for the button.
        """
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)

    def is_pressed(self) -> bool:
        """
        Check if the button is pressed.
        """
        state = GPIO.input(self.pin) == GPIO.LOW
        return state


BUTTON = Button(7)
