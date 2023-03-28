"""
Display a clock on the circular displays.
Author: Benjamin Dodd (1901386)
"""

import time
import datetime
from enum import Enum

from . import LOGGER
from ..display.circular_display import LEFT_DISPLAY, RIGHT_DISPLAY
from ..threading.worker_manager import WORKER_MANAGER
from ..threading.worker_thread import WorkerThread
from ..button.button_repository import BUTTON_REPOSITORY
from ..button.button import BUTTON

class ClockMode(Enum):
    """
    The clock mode.
    """
    HOUR_24 = 0
    HOUR_12 = 1

class Clock:

    class ClockWorker(WorkerThread):
        """
        Displays the current time on the circular display.
        """

        def __init__(self, clock: "Clock"):
            super().__init__()
            self.clock = clock

        def work(self):
            while not self.is_stopped():
                now = datetime.datetime.now()
                hour = now.hour
                minute = now.minute

                if self.clock.mode == ClockMode.HOUR_12:
                    if hour > 12:
                        hour -= 12

                RIGHT_DISPLAY.display_number(hour)
                LEFT_DISPLAY.display_number(minute)
                time.sleep(1)

    class ClockModeWorker(WorkerThread):
        """
        Displays the current time on the circular display.
        """

        def __init__(self, clock: "Clock"):
            super().__init__()
            self.clock = clock

        def work(self):
            while not self.is_stopped():
                if BUTTON_REPOSITORY.button_state:
                    if self.clock.mode == ClockMode.HOUR_12:
                        self.clock.mode = ClockMode.HOUR_24
                    else:
                        self.clock.mode = ClockMode.HOUR_12
                    LOGGER.debug("Clock mode changed to %s", self.clock.mode)
                while BUTTON_REPOSITORY.button_state:
                    time.sleep(0.1)
                time.sleep(1)

    def __init__(self):
        self.running = False
        self.mode = ClockMode.HOUR_24

        self.clock_worker = self.ClockWorker(self)
        self.clock_mode_worker = self.ClockModeWorker(self)

    def start(self):
        """
        Starts the clock.
        """
        LOGGER.info("Starting clock")
        self.running = True
        self.clock_worker = self.ClockWorker(self)
        self.clock_mode_worker = self.ClockModeWorker(self)
        WORKER_MANAGER.add_worker(self.clock_worker)
        WORKER_MANAGER.add_worker(self.clock_mode_worker)
        self.run()

    def stop(self):
        """
        Stops the clock.
        """
        LOGGER.info("Stopping clock")
        self.running = False
        WORKER_MANAGER.remove_worker(self.clock_worker)
        WORKER_MANAGER.remove_worker(self.clock_mode_worker)

    def run(self):
        """
        Starts the clock.
        """
        while self.running:
            time.sleep(1)

CLOCK = Clock()

if __name__ == "__main__":
    try:
        LOGGER.debug("Starting clock")
        CLOCK.start()
    except KeyboardInterrupt:
        CLOCK.stop()
        LOGGER.debug("Exiting clock")
    WORKER_MANAGER.stop_all_workers()
