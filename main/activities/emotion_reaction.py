"""
Display emotions on the circular display based on the current detected emotion.
Author: Benjamin Dodd (1901386)
"""

import time
from os import path
import cv2 as cv

from . import LOGGER
from ..camera.video_feed import VIDEO_FEED
from ..camera.emotion_detection import EMOTION_DETECTION
from ..camera.emotion_repository import EMOTION_REPOSITORY
from ..display.circular_display import LEFT_DISPLAY, RIGHT_DISPLAY
from ..threading.worker_manager import WORKER_MANAGER
from ..threading.worker_thread import WorkerThread


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

class EmotionReaction:

    class EmotionWorker(WorkerThread):
        """
        Uses the camera feed and gives the image to the emotion detection class.
        """
        def work(self):
            while not self.is_stopped():
                capture = VIDEO_FEED.capture()
                if capture is not None:
                    EMOTION_DETECTION.image = capture
                time.sleep(0.15)

    class DisplayWorker(WorkerThread):
        """
        Displays the current emotion on the circular display in the form of an image.
        """
        def work(self):
            RIGHT_DISPLAY.image = IMAGES["happy"]
            LEFT_DISPLAY.image = cv.flip(IMAGES["happy"], 1)
            while not self.is_stopped():
                emotion = EMOTION_REPOSITORY.current_emotion
                if emotion is not None:
                    RIGHT_DISPLAY.image = IMAGES[emotion]
                    LEFT_DISPLAY.image = cv.flip(IMAGES[emotion], 1)
                time.sleep(0.15)

    def __init__(self):
        self.running = False
        self.emotion_worker = self.EmotionWorker()
        self.display_worker = self.DisplayWorker()

    def start(self):
        WORKER_MANAGER.add_worker(self.emotion_worker)
        WORKER_MANAGER.add_worker(self.display_worker)
        self.running = True
        self.run()

    def stop(self):
        LOGGER.debug("Stopping emotion reaction game")
        self.running = False

    def run(self):
        while self.running:
            time.sleep(0.15)

    def __str__(self):
        return "Emotion Reaction"

    def __repr__(self):
        return self.__str__()

EMOTION_REACTION = EmotionReaction()

if __name__ == "__main__":
    try:
        EMOTION_REACTION.start()
    except KeyboardInterrupt:
        EMOTION_REACTION.stop()
        LOGGER.debug("Exiting emotion reaction game")
        WORKER_MANAGER.stop_all_workers()
