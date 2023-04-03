"""
Main activity that allows the user to select which activity to run.
Author: Benjamin Dodd (1901386)
"""

import time
from typing import List

from . import LOGGER

from .activity import Activity

from ..display.circular_display import LeftDisplay, RightDisplay
from ..button.button import Button

from ..threading.worker_manager import WorkerManager
from ..threading.worker_thread import WorkerThread

class StopActivity(WorkerThread):
    """
    Worker that will stop the current activity if the button is pressed for 8 seconds.
    """

    def __init__(self, activity: Activity, button: Button):
        super().__init__()
        self.running = True
        self.activity = activity
        self.button = button

    def work(self):
        while self.running:
            if self.button.has_been_pressed_for(8):
                self.activity.stop()
                self.running = False
            time.sleep(0.1)

class ActivitySelector(Activity):
    """
    Main activity that allows the user to select which activity to run.
    """

    def __init__(self, worker_manager: WorkerManager, activities: List[Activity], left_display: LeftDisplay, right_display: RightDisplay, button: Button):
        super().__init__("activity_selector", worker_manager)
        self.activities = activities
        self.left_display = left_display
        self.right_display = right_display
        self.button = button

        self.current_activity_index = 0

    def work(self):
        while self.running:
            self.left_display.display_number(self.current_activity_index + 1)
            self.right_display.display_text(self.activities[self.current_activity_index].name)

            if self.button.has_been_pressed_for(8):
                LOGGER.debug("Stopping activity selector")
                self.running = False
            if self.button.has_been_pressed_for(3):
                LOGGER.debug("Starting activity %s", self.activities[self.current_activity_index])
                self.activities[self.current_activity_index].start()
                self.worker_manager.add_worker(StopActivity(self.activities[self.current_activity_index], self.button))
                self.activities[self.current_activity_index].join()
            else:
                if self.button.is_pressed():
                    self.current_activity_index = (self.current_activity_index + 1) % len(self.activities)
                    LOGGER.debug("Changing activity to %s", self.activities[self.current_activity_index])

            time.sleep(0.1)
