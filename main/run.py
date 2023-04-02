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


from .threading import worker_manager

BUTTON = Button("main", 37)
STEPPER_MOTOR = StepperMotor()

LEFT_DISPLAY = LeftDisplay()
RIGHT_DISPLAY = RightDisplay()

VIDEO_FEED = VideoFeed()
GESTURE_DETECTION = GestureDetection()
EMOTION_DETECTION = EmotionDetection()
