"""
Main activity that allows the user to select which activity to run.
Author: Benjamin Dodd (1901386)
"""

import time
from typing import List

from main.activities import LOGGER

from main.activities.activity import Activity

from main.display.circular_display import LeftDisplay, RightDisplay
from main.button.button import Button

from main.threading.worker_manager import WorkerManager
from main.threading.worker_thread import Worker

START_TIME = 3
STOP_TIME = 6

class StopActivity(Worker):
    """
    Worker that will stop the current activity if the button is pressed for 8 seconds.
    """

    def __init__(self, activity: Activity, button: Button):
        super().__init__()
        self.activity = activity
        self.button = button

    def work(self):
        LOGGER.debug("Starting stop-wait activity")
        while not self.is_stopped():
            if self.button.is_pressed():
                self.button.wait_for_release()
                if self.button.has_been_pressed_for(STOP_TIME):
                    LOGGER.debug("Stopping activity %s", self.activity)
                    self.activity.stop()
                    self.stop()
            time.sleep(0.1)

class ActivitySelector(Activity):
    """
    Main activity that allows the user to select which activity to run.
    """

    def __init__(self, activities: List[Activity], left_display: LeftDisplay, right_display: RightDisplay, button: Button):
        super().__init__("activity_selector")
        self.activities = activities
        self.left_display = left_display
        self.right_display = right_display
        self.button = button

        self.current_activity_index = 0

    def work(self):
        LOGGER.debug("Starting activity selector")
        while not self.is_stopped():
            self.left_display.display_number(self.current_activity_index + 1)
            self.right_display.display_text(self.activities[self.current_activity_index].name)

            if self.button.is_pressed():
                self.button.wait_for_release()
                if self.button.has_been_pressed_for(STOP_TIME):
                    LOGGER.debug("Stopping activity selector")
                    self.stop()
                elif self.button.has_been_pressed_for(START_TIME):
                    LOGGER.debug("Starting activity %s", self.activities[self.current_activity_index])
                    self.activities[self.current_activity_index].start()
                    stop_activity = StopActivity(self.activities[self.current_activity_index], self.button)
                    stop_activity.start()
                    self.activities[self.current_activity_index].join()
                else:
                    self.current_activity_index = (self.current_activity_index + 1) % len(self.activities)
                    self.left_display.display_text(self.activities[self.current_activity_index].name)
                    LOGGER.debug("Changing activity to %s", self.activities[self.current_activity_index])

            time.sleep(0.1)
