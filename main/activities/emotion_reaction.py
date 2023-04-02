"""
Display emotions on the circular display based on the current detected emotion.
Author: Benjamin Dodd (1901386)
"""

import time
from os import path
import cv2 as cv


from .activity import Activity

from ..threading.worker_manager import WorkerManager
from ..display.circular_display import LeftDisplay, RightDisplay
from ..camera.emotion_detection import EmotionDetection
from ..camera.video_feed import VideoFeed

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

    def __init__(self, worker_manager: WorkerManager, left_display: LeftDisplay, right_display: RightDisplay, emotion_detection: EmotionDetection, video_feed: VideoFeed):
        super().__init__("EmotionReaction", worker_manager)
        self.left_display = left_display
        self.right_display = right_display
        self.emotion_detection = emotion_detection
        self.video_feed = video_feed
        self.left_display.image = IMAGES["neutral"]
        self.right_display.image = IMAGES["neutral"]

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
            time.sleep(0.15)
