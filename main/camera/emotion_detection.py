"""
Emotion detection using OpenCV and SkiKit
Author: Benjamin Dodd (1901386)
"""

import threading
import cv2 as cv

from fer import FER

from . import LOGGER

from .emotion_repository import EMOTION_REPOSITORY
from .video_feed import VideoFrame

from ..threading.worker_manager import WORKER_MANAGER
from ..threading.worker_thread import WorkerThread
from ..util.singleton import Singleton

class EmotionDetection(metaclass=Singleton):
    """
    Class for detecting emotions in a video frame.
    """

    class EmotionDetectionWorker(WorkerThread):
        """
        Worker thread for the emotion detection.
        """
        running = False

        def __init__(self, emotion_detection: "EmotionDetection"):
            """Create a new instance of the EmotionDetectionWorker class."""
            super().__init__()
            self.detector = FER()
            self.emotion_detection = emotion_detection

        def work(self):
            """
            Run the worker thread.
            """
            if self.running or self.emotion_detection.image is None:
                LOGGER.debug("Emotion detection worker thread is already running or no image to analyse.")
                return
            try:
                self.running = True
                dominant_emotion, _ = self.detector.top_emotion(self.emotion_detection.image)
                EMOTION_REPOSITORY.current_emotion = dominant_emotion
            except cv.error:
                return

    def __init__(self):
        super().__init__()
        self.__lock = threading.Lock()
        self.__image = None

    @property
    def image(self):
        """
        Get the image to analyse.
        """
        with self.__lock:
            return self.__image

    @image.setter
    def image(self, frame: VideoFrame):
        """
        Set the image to analyse.
        """
        with self.__lock:
            self.__image = frame.image
            worker = self.EmotionDetectionWorker(self)
            WORKER_MANAGER.add_worker(worker)

EMOTION_DETECTION = EmotionDetection()

if __name__ == "__main__":
    from .video_feed import VIDEO_FEED

    while True:
        video_frame = VIDEO_FEED.capture()
        if video_frame:
            EMOTION_DETECTION.image = video_frame
            # draw the emotion on the frame
            current_emotion = EMOTION_REPOSITORY.current_emotion
            cv.putText(video_frame.image, EMOTION_REPOSITORY.current_emotion, (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv.imshow('Video', video_frame.image)
        if cv.waitKey(1) & 0xFF == ord('q'):
            WORKER_MANAGER.stop_all_workers()
            break
