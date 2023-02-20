"""
Number guessing game where the user has to gesture with their fingers to guess the number.
Author: Benjamin Dodd (1901386)
"""

import cv2 as cv
import time
from random import randint

from . import LOGGER
from ..camera.video_feed import VIDEO_FEED
from ..camera.gesture_detection import GESTURE_DETECTION
from ..camera.gesture_repository import GESTURE_REPOSITORY
from ..display.circular_display import LEFT_DISPLAY, RIGHT_DISPLAY
from ..util.singleton import Singleton
from ..threading.worker_manager import WORKER_MANAGER
from ..threading.worker_thread import WorkerThread

class NumberGuessing(metaclass=Singleton):

    class NumberGuessingWorker(WorkerThread):

        def __init__(self, number_guessing: "NumberGuessing"):
            super().__init__()
            self.number_guessing = number_guessing

        def work(self):
            if self.number_guessing.is_running:
                self.number_guessing.run()

    def __init__(self):
        self.number = randint(1, 8)
        self.guess = -1
        self.is_running = False
        self.worker = self.NumberGuessingWorker(self)

    def start(self):
        self.is_running = True
        WORKER_MANAGER.add_thread(self.worker)

    def stop(self):
        self.is_running = False
        WORKER_MANAGER.delete_thread(self.worker)

    def run(self):
        LEFT_DISPLAY.image = VIDEO_FEED.capture().image
        RIGHT_DISPLAY.display_number(self.number)
        while self.guess != self.number:
            self.guess = GESTURE_REPOSITORY.current_gesture
            if self.guess == self.number:
                LOGGER.info("Correct!")
                self.stop()
            else:
                LOGGER.info("Incorrect! Try again.")

            while self.guess == GESTURE_REPOSITORY.current_gesture:
                time.sleep(0.15)

            LEFT_DISPLAY.image = VIDEO_FEED.capture().image
            RIGHT_DISPLAY.display_number(self.number)

        self.stop()

NUMBER_GUESSING = NumberGuessing()

if __name__ == "__main__":
    import sys
    NUMBER_GUESSING.start()
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        NUMBER_GUESSING.stop()
        WORKER_MANAGER.stop_threads()
