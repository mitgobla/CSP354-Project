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
    EMULATION = False
    import RPi.GPIO as GPIO
except ImportError:
    EMULATION = True
    from main.util.mock_gpio import MockGPIO as GPIO

from main.threading.worker_thread import Worker

class ButtonEmulator(Worker):

    def __init__(self, button: "Button", debug: bool = False):
        super().__init__()
        self.button = button
        self.debug = debug

    def work(self):
        while not self.is_stopped():
            user_input = input("Is button pressed: ")
            user_input = user_input.lower()
            if user_input == "y":
                self.button._state = True
                self.button.start_press_time = time.time()
            else:
                self.button._state = False
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

        if EMULATION:
            self.emulator = ButtonEmulator(self)
            self.emulator.start()

    def __repr__(self):
        return f"Button({self.name}, {self.pin})"

    def __str__(self):
        return self.__repr__()

    def _setup(self):
        """
        Set up the GPIO pins for the button.
        """
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        GPIO.add_event_detect(self.pin, GPIO.BOTH, callback = self._update_state, bouncetime = 200)

    def _update_state(self):
        with self._lock:
            LOGGER.debug(f"Button {self.name} has been pressed")
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

    def is_pressed(self):
        """
        Check if the button is pressed.
        """
        return self.state

    def wait_for_press(self):
        """
        Wait for the button to be pressed.
        """
        while not self.state:
            pass
        LOGGER.debug(f"Button {self.name} has been pressed")

    def wait_for_release(self):
        """
        Wait for the button to be released.
        """
        while self.state:
            pass
        LOGGER.debug(f"Button {self.name} has been released")

    def has_been_pressed_for(self, seconds: float):
        """
        Check if the button has been pressed for a given amount of time.
        """
        LOGGER.debug(f"Button {self.name} has been pressed for {time.time() - self.start_press_time} seconds")
        return time.time() - self.start_press_time >= seconds
