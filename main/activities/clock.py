"""
Clock activity
Author: Benjamin Dodd (1901386)
"""
import time
from enum import Enum
from datetime import datetime

from .activity import Activity

from ..display.circular_display import LeftDisplay, RightDisplay
from ..button.button import Button

from ..threading.worker_manager import WorkerManager

class ClockMode(Enum):
    """
    Enum for the different clock modes.
    """
    CLOCK_12_HOUR = 0
    CLOCK_24_HOUR = 1

class ClockActivity(Activity):
    """
    Clock activity
    Displays the hour and minute on the circular displays.
    Button is used to change the clock mode.
    """

    def __init__(self, worker_manager: WorkerManager, left_display: LeftDisplay, right_display: RightDisplay, button: Button):
        super().__init__("clock", worker_manager)
        self.left_display = left_display
        self.right_display = right_display
        self.button = button

        self.mode = ClockMode.CLOCK_12_HOUR

    def work(self):
        while self.running:
            current_time = self.get_time()
            self.left_display.display_number(current_time[0])
            self.right_display.display_number(current_time[1])

            if self.button.is_pressed():
                self.change_mode()
            time.sleep(1)

    def get_time(self):
        """
        Gets the current time.
        """
        if self.mode == ClockMode.CLOCK_12_HOUR:
            hour, minute = datetime.now().strftime("%I:%M").split(":")
        else:
            hour, minute = datetime.now().strftime("%H:%M").split(":")
        return (hour, minute)

    def change_mode(self):
        """
        Changes the clock mode.
        """
        self.mode = ClockMode.CLOCK_24_HOUR if self.mode == ClockMode.CLOCK_12_HOUR else ClockMode.CLOCK_12_HOUR
