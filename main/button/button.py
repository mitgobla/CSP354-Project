"""
Driver class for a button.
Author: Benjamin Dodd (1901386)
"""

from . import LOGGER
from .button_repository import ButtonRepository

try:
    import RPi.GPIO as GPIO
except ImportError:
    from ..util.mock_gpio import MockGPIO as GPIO

class Button:
    """
    Driver class for a button.
    """

    def __init__(self, pin: int):
        """Create a new instance of the Button class."""
        self.pin = pin
        self.button_repository = ButtonRepository()
        self._setup()

    def __repr__(self):
        return f"Button({self.pin})"

    def __str__(self):
        return f"Button({self.pin})"

    def _setup(self):
        """
        Set up the GPIO pins for the button.
        """
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        GPIO.add_event_detect(self.pin, GPIO.BOTH, callback = self._update_repository, bouncetime = 200)

        if not self.button_repository.has_button(self):
            self.button_repository.update_button_state(self, False)

    def _update_repository(self):
        LOGGER.debug("Updating button state for %s", self)
        self.button_repository.update_button_state(self, not GPIO.input(self.pin))

