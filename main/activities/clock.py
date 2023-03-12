"""
Display a clock on the circular displays.
Author: Benjamin Dodd (1901386)
"""

import time
import datetime
import cv2 as cv

from . import LOGGER
from ..display.circular_display import LEFT_DISPLAY, RIGHT_DISPLAY
from ..util.singleton import Singleton
from ..threading.worker_manager import WORKER_MANAGER
from ..threading.worker_thread import WorkerThread

class Clock(metaclass=Singleton):

    class ClockWorker(WorkerThread):
        """
        Displays the current time on the circular display.
        """
        def work(self):
            while not self.is_stopped():
                now = datetime.datetime.now()
                hour = now.hour
                minute = now.minute
                RIGHT_DISPLAY.display_number(hour)
                LEFT_DISPLAY.display_number(minute)
                time.sleep(60 - now.second)

    def __init__(self):
        self.running = False
        self.clock_worker = self.ClockWorker()

    def start(self):
        """
        Starts the clock.
        """
        LOGGER.info("Starting clock")
        self.running = True
        WORKER_MANAGER.add_worker(self.clock_worker)
        self.run()

    def stop(self):
        """
        Stops the clock.
        """
        LOGGER.info("Stopping clock")
        self.running = False
        WORKER_MANAGER.remove_worker(self.clock_worker)

    def run(self):
        """
        Starts the clock.
        """
        while self.running:
            time.sleep(1)

CLOCK = Clock()

if __name__ == "__main__":
    try:
        CLOCK.start()
    except KeyboardInterrupt:
        CLOCK.stop()
        LOGGER.debug("Exiting clock")
        WORKER_MANAGER.stop_all_workers()
