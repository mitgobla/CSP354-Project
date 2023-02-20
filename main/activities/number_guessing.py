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

    class LeftDisplayWorker(WorkerThread):
        def work(self):
            while not self.is_stopped():
                capture = VIDEO_FEED.capture()
                if capture is not None:
                    LEFT_DISPLAY.image = capture.image
                    GESTURE_DETECTION.image = capture
                time.sleep(0.15)

    class RightDisplayWorker(WorkerThread):

        def __init__(self, number_guessing: "NumberGuessing"):
            super().__init__()
            self.number_guessing = number_guessing

        def work(self):
            old_gesture = 0
            while not self.is_stopped():
                if GESTURE_REPOSITORY.current_gesture == old_gesture:
                    continue
                old_gesture = GESTURE_REPOSITORY.current_gesture
                if GESTURE_REPOSITORY.current_gesture == self.number_guessing.number:
                    RIGHT_DISPLAY.display_number(GESTURE_REPOSITORY.current_gesture, (0, 255, 0))
                else:
                    RIGHT_DISPLAY.display_number(GESTURE_REPOSITORY.current_gesture, (0, 0, 255))
                time.sleep(0.15)

    def __init__(self):
        self.number = randint(1, 8)
        LOGGER.debug("Number to guess: %s", self.number)
        self.guess = 0
        self.running = False

        self.left_display_worker = self.LeftDisplayWorker()
        self.right_display_worker = self.RightDisplayWorker(self)


    def start(self):
        WORKER_MANAGER.add_thread(self.left_display_worker)
        WORKER_MANAGER.add_thread(self.right_display_worker)
        self.running = True
        self.run()

    def stop(self):
        self.running = False
        WORKER_MANAGER.delete_thread(self.left_display_worker)
        WORKER_MANAGER.delete_thread(self.right_display_worker)

    def run(self):
        while self.running:
            while self.guess != self.number:
                self.guess = GESTURE_REPOSITORY.current_gesture
                LOGGER.info("Incorrect! Try again.")
                while self.guess == GESTURE_REPOSITORY.current_gesture:
                    time.sleep(0.15)

            LOGGER.info("Correct! The number was %s", self.number)
            self.stop()

NUMBER_GUESSING = NumberGuessing()

if __name__ == "__main__":
    NUMBER_GUESSING.start()
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        NUMBER_GUESSING.stop()
        WORKER_MANAGER.stop_threads()
