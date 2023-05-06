"""
Driver class for a button.

Portions of this code were produced from the examples in the LABISTS Starter Kit User Manual:
LABISTS, “Raspberry Pi Starter Kit Tutorial,” [Online]. Available: https://labists.com/pages/starter-kit-tutorial. [Accessed 12 February 2023].

Author: Benjamin Dodd (1901386)
"""
import time
from threading import Lock

from main.button import LOGGER

try:
    import RPi.GPIO as GPIO
except ImportError:
    from main.util.mock_gpio import MockGPIO as GPIO

class Button:
    """
    Driver class for a button.
    """

    def __init__(self, name: str, pin: int):
        """Create a new instance of the Button class."""

        self.name = name
        self.pin = pin
        self.start_press_time = 0

        self._lock = Lock()
        self._state = False
        self._setup()

    def __repr__(self):
        return f"Button({self.name}, {self.pin})"

    def __str__(self):
        return self.__repr__()

    def _setup(self):
        """
        Set up the GPIO pins for the button.
        """
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        GPIO.add_event_detect(self.pin, GPIO.BOTH, callback = self._update_state, bouncetime = 200)

    def _update_state(self):
        with self._lock:
            self._state = not GPIO.input(self.pin)
            if self._state:
                self.start_press_time = time.time()


    @property
    def state(self):
        """
        Get the current state of the button.
        """
        with self._lock:
            return self._state

    def wait_for_press(self):
        """
        Wait for the button to be pressed.
        """
        while not self.state:
            pass

    def wait_for_release(self):
        """
        Wait for the button to be released.
        """
        while self.state:
            pass

    def has_been_pressed_for(self, seconds: float):
        """
        Check if the button has been pressed for a given amount of time.
        """
        return self.state and time.time() - self.start_press_time >= seconds
