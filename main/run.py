"""
Main script to run the application
Author: Benjamin Dodd (1901386)
"""

from . import LOGGER, IS_RASPBERRY_PI

from .button.button import Button
from .motor.stepper_motor import StepperMotor
from .display.circular_display import LeftDisplay, RightDisplay
from .camera.video_feed import VideoFeed
from .camera.gesture_detection import GestureDetection
from .camera.emotion_detection import EmotionDetection

from .activities.clock import ClockActivity

from .threading.worker_manager import WorkerManager

WORKER_MANAGER = WorkerManager()

BUTTON = Button("main", 37)
STEPPER_MOTOR = StepperMotor(WORKER_MANAGER)

LEFT_DISPLAY = LeftDisplay(WORKER_MANAGER)
RIGHT_DISPLAY = RightDisplay(WORKER_MANAGER)

VIDEO_FEED = VideoFeed()
GESTURE_DETECTION = GestureDetection(WORKER_MANAGER)
EMOTION_DETECTION = EmotionDetection(WORKER_MANAGER)

CLOCK_ACTIVITY = ClockActivity(WORKER_MANAGER, LEFT_DISPLAY, RIGHT_DISPLAY, BUTTON)
