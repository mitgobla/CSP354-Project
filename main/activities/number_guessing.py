"""
Number guessing game where the user has to gesture with their fingers to guess the number.
Author: Benjamin Dodd (1901386)
"""

import time
from random import randint

from main.activities.activity import Activity

from main.threading.worker_manager import WorkerManager
from main.display.circular_display import LeftDisplay, RightDisplay
from main.camera.gesture_detection import GestureDetection
from main.camera.video_feed import VideoFeed

class NumberGuessingActivity(Activity):
    """
    Number guessing game where the user has to gesture with their fingers to guess the number.
    """

    def __init__(self, left_display: LeftDisplay, right_display: RightDisplay, video_feed: VideoFeed, gesture_detection: GestureDetection):
        super().__init__("NumberGuessing")
        self.left_display = left_display
        self.right_display = right_display
        self.video_feed = video_feed
        self.gesture_detection = gesture_detection

        self.random_number = randint(1, 8)

    def work(self):
        while not self.is_stopped():
            capture = self.video_feed.capture()
            self.gesture_detection.image = capture
            finger_count = self.gesture_detection.finger_count
            correct_guess = finger_count == self.random_number
            colour = (0, 255, 0) if correct_guess else (0, 0, 255)
            if finger_count is not None:
                self.left_display.display_number(finger_count, colour)
                self.right_display.image = capture.image
            else:
                self.left_display.display_number(0, colour)
                self.right_display.image = capture.image

            if correct_guess:
                self.random_number = randint(1, 8)
                time.sleep(3)

            time.sleep(0.15)
