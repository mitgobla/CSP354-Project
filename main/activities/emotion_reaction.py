"""
Display emotions on the circular display based on the current detected emotion.
Author: Benjamin Dodd (1901386)
"""

import time
from os import path
import cv2 as cv


from main.activities.activity import Activity

from main.threading.worker_manager import WorkerManager
from main.display.circular_display import LeftDisplay, RightDisplay
from main.camera.emotion_detection import EmotionDetection
from main.camera.video_feed import VideoFeed, CAMERA_WIDTH
from main.motor.stepper_motor import StepperMotor

IMAGE_PATH = path.join("res", "emotion")

IMAGES = {
    "happy": cv.imread(path.join(IMAGE_PATH, "happy.png")),
    "sad": cv.imread(path.join(IMAGE_PATH, "sad.png")),
    "angry": cv.imread(path.join(IMAGE_PATH, "angry.png")),
    "disgust": cv.imread(path.join(IMAGE_PATH, "disgust.png")),
    "fear": cv.imread(path.join(IMAGE_PATH, "fear.png")),
    "surprise": cv.imread(path.join(IMAGE_PATH, "surprise.png")),
    "neutral": cv.imread(path.join(IMAGE_PATH, "neutral.png"))
}

class EmotionReactionActivity(Activity):
    """
    Class for displaying emotions on the circular display based on the current detected emotion.
    """

    def __init__(self, worker_manager: WorkerManager, left_display: LeftDisplay, right_display: RightDisplay, emotion_detection: EmotionDetection, video_feed: VideoFeed, stepper_motor: StepperMotor):
        super().__init__("EmotionReaction", worker_manager)
        self.left_display = left_display
        self.right_display = right_display
        self.emotion_detection = emotion_detection
        self.video_feed = video_feed
        self.left_display.image = IMAGES["neutral"]
        self.right_display.image = IMAGES["neutral"]
        self.stepper_motor = stepper_motor

    def work(self):
        while self.running:
            capture = self.video_feed.capture()
            self.emotion_detection.image = capture
            emotion = self.emotion_detection.current_emotion
            if emotion is not None:
                self.left_display.image = IMAGES[emotion]
                self.right_display.image = IMAGES[emotion]
            else:
                self.left_display.image = IMAGES["neutral"]
                self.right_display.image = IMAGES["neutral"]
            face_position = self.emotion_detection.face_position
            if face_position is not None:
                face_center = face_position[0] + (face_position[2] / 2)
                if face_center < (CAMERA_WIDTH / 2):
                    # 45 max turn left
                    # percentage of how far left the face is
                    percentage = (face_center / (CAMERA_WIDTH / 2)) * 45
                    self.stepper_motor.rotate_to(percentage)
                else:
                    # 45 max turn right
                    # percentage of how far right the face is
                    percentage = ((face_center - (CAMERA_WIDTH / 2)) / (CAMERA_WIDTH / 2)) * 45
                    self.stepper_motor.rotate_to(-percentage)
            time.sleep(0.15)
