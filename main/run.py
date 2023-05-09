"""
Main script to run the application
Author: Benjamin Dodd (1901386)
"""

import sys

from main import LOGGER, IS_RASPBERRY_PI, ARGS

from main.button.button import Button
from main.motor.stepper_motor import StepperMotor
from main.display.circular_display import LeftDisplay, RightDisplay
from main.camera.video_feed import VideoFeed
from main.camera.gesture_detection import GestureDetection
from main.camera.emotion_detection import EmotionDetection

from main.activities.clock import ClockActivity
from main.activities.emotion_reaction import EmotionReactionActivity
from main.activities.number_guessing import NumberGuessingActivity
from main.activities.activity_selector import ActivitySelector

from main.threading.worker_manager import WorkerManager
from main.threading.worker_thread import Worker

WORKER_MANAGER = WorkerManager()

Worker.set_manager(WORKER_MANAGER)

BUTTON = Button("main", 13)
STEPPER_MOTOR = StepperMotor()

LEFT_DISPLAY = LeftDisplay()
RIGHT_DISPLAY = RightDisplay()

VIDEO_FEED = VideoFeed()
GESTURE_DETECTION = GestureDetection()
EMOTION_DETECTION = EmotionDetection()

CLOCK_ACTIVITY = ClockActivity(LEFT_DISPLAY, RIGHT_DISPLAY, BUTTON)
EMOTION_REACTION_ACTIVITY = EmotionReactionActivity(LEFT_DISPLAY, RIGHT_DISPLAY, EMOTION_DETECTION, VIDEO_FEED, STEPPER_MOTOR)
NUMBER_GUESSING_ACTIVITY = NumberGuessingActivity(LEFT_DISPLAY, RIGHT_DISPLAY, VIDEO_FEED, GESTURE_DETECTION)

ACTIVITIES = [CLOCK_ACTIVITY, EMOTION_REACTION_ACTIVITY, NUMBER_GUESSING_ACTIVITY]
ACTIVITY_SELECTOR = ActivitySelector(ACTIVITIES, LEFT_DISPLAY, RIGHT_DISPLAY, BUTTON)

def raspberry_pi_main():
    """
    Main function to run the application
    """
    LOGGER.info("Starting application on Raspberry Pi")
    ACTIVITY_SELECTOR.start()
    LOGGER.info("Application started on Raspberry Pi")
    ACTIVITY_SELECTOR.join()
    WORKER_MANAGER.stop_all_workers()
    LOGGER.info("Application stopped on Raspberry Pi")

def emulator_main():
    from PyQt5.QtWidgets import QApplication
    from main.ui.run import MainWindow
    APPLICATION = QApplication(sys.argv)
    WINDOW = MainWindow()
    """
    Main function to run the application in an emulator
    """
    LOGGER.info("Starting application in emulator")
    WINDOW.show()
    sys.exit(APPLICATION.exec_())

if __name__ == "__main__":
    if IS_RASPBERRY_PI or not ARGS.emulate:
        raspberry_pi_main()
    else:
        emulator_main()
