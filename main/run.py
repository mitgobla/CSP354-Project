"""
Main script to run the application
Author: Benjamin Dodd (1901386)
"""

import sys
from PyQt5.QtWidgets import QApplication

from . import LOGGER, IS_RASPBERRY_PI

from .button.button import Button
from .motor.stepper_motor import StepperMotor
from .display.circular_display import LeftDisplay, RightDisplay
from .camera.video_feed import VideoFeed
from .camera.gesture_detection import GestureDetection
from .camera.emotion_detection import EmotionDetection

from .activities.clock import ClockActivity
from .activities.emotion_reaction import EmotionReactionActivity
from .activities.number_guessing import NumberGuessingActivity
from .activities.activity_selector import ActivitySelector

from .threading.worker_manager import WorkerManager

from .ui.run import MainWindow

WORKER_MANAGER = WorkerManager()

BUTTON = Button("main", 37)
STEPPER_MOTOR = StepperMotor(WORKER_MANAGER)

LEFT_DISPLAY = LeftDisplay(WORKER_MANAGER)
RIGHT_DISPLAY = RightDisplay(WORKER_MANAGER)

VIDEO_FEED = VideoFeed()
GESTURE_DETECTION = GestureDetection(WORKER_MANAGER)
EMOTION_DETECTION = EmotionDetection(WORKER_MANAGER)

CLOCK_ACTIVITY = ClockActivity(WORKER_MANAGER, LEFT_DISPLAY, RIGHT_DISPLAY, BUTTON)
EMOTION_REACTION_ACTIVITY = EmotionReactionActivity(WORKER_MANAGER, LEFT_DISPLAY, RIGHT_DISPLAY, EMOTION_DETECTION, VIDEO_FEED)
NUMBER_GUESSING_ACTIVITY = NumberGuessingActivity(WORKER_MANAGER, LEFT_DISPLAY, RIGHT_DISPLAY, VIDEO_FEED, GESTURE_DETECTION)

ACTIVITIES = [CLOCK_ACTIVITY, EMOTION_REACTION_ACTIVITY, NUMBER_GUESSING_ACTIVITY]
ACTIVITY_SELECTOR = ActivitySelector(WORKER_MANAGER, ACTIVITIES, LEFT_DISPLAY, RIGHT_DISPLAY, BUTTON)

def raspberry_pi_main():
    """
    Main function to run the application
    """
    LOGGER.info("Starting application")
    ACTIVITY_SELECTOR.start()
    LOGGER.info("Application started")
    ACTIVITY_SELECTOR.join()
    WORKER_MANAGER.stop_all_workers()

APPLICATION = QApplication(sys.argv)
WINDOW = MainWindow()

def emulator_main():
    """
    Main function to run the application in an emulator
    """
    LOGGER.info("Starting application")
    WINDOW.show()
    sys.exit(APPLICATION.exec_())

if __name__ == "__main__":
    if IS_RASPBERRY_PI:
        raspberry_pi_main()
    else:
        emulator_main()
