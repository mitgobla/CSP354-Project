"""
Emotion detection using OpenCV and SkiKit
Author: Benjamin Dodd (1901386)
"""

import threading
import cv2 as cv

from fer import FER

from . import LOGGER

from .video_feed import VideoFrame

from ..threading.worker_manager import WorkerManager
from ..threading.worker_thread import WorkerThread

DETECTOR = FER()

class EmotionDetection:
    """
    Class for detecting emotions in a video frame.
    """

    _lock = threading.Lock()
    _image = None
    _dominant_emotion = None
    _face_position = None

    _instance = None
    _instance_lock = threading.Lock()
    _intitialized = False

    def __new__(cls, worker_manager: WorkerManager):
        if cls._instance is None:
            with cls._instance_lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, worker_manager: WorkerManager):
        if not self._intitialized:
            self.worker_manager = worker_manager
            self.worker = None
            self._intitialized = True

    @property
    def image(self):
        """
        Get the image to analyse.
        """
        with self._lock:
            return self._image

    @image.setter
    def image(self, frame: VideoFrame):
        """
        Set the image to analyse.
        """
        with self._lock:
            if self.worker is not None:
                if self.worker.is_running():
                    return

            self._image = frame.image
            self.worker = EmotionDetectionWorker(self)
            self.worker_manager.add_worker(self.worker)

    @property
    def current_emotion(self):
        """
        Get the dominant emotion.
        """
        with self._lock:
            return self._dominant_emotion

    @current_emotion.setter
    def current_emotion(self, emotion: str):
        """
        Set the dominant emotion.
        """
        with self._lock:
            self._dominant_emotion = emotion

    @property
    def face_position(self):
        """
        Get the position of the face.
        """
        with self._lock:
            return self._face_position

    @face_position.setter
    def face_position(self, position: tuple):
        """
        Set the position of the face.
        """
        with self._lock:
            self._face_position = position

class EmotionDetectionWorker(WorkerThread):
    """
    Worker thread for the emotion detection.
    """
    _running = False

    def __init__(self, emotion_detection: EmotionDetection):
        """Create a new instance of the EmotionDetectionWorker class."""
        super().__init__()
        self.emotion_detection = emotion_detection

    def is_running(self):
        """
        Check if the worker thread is running.
        """
        return self._running

    def work(self):
        """
        Run the worker thread.
        """
        if self._running or self.emotion_detection.image is None:
            return

        try:
            self._running = True
            dominant_emotion, _ = DETECTOR.top_emotion(self.emotion_detection.image)
            face_position = DETECTOR.find_faces(self.emotion_detection.image)[0]
            self.emotion_detection.current_emotion = dominant_emotion
            self.emotion_detection.face_position = face_position
        except cv.error:
            self._running = False
            return
        self._running = False

if __name__ == "__main__":
    from .video_feed import VideoFeed

    WORKER_MANAGER = WorkerManager()
    VIDEO_FEED = VideoFeed()
    EMOTION_DETECTION = EmotionDetection(WORKER_MANAGER)

    while True:
        video_frame = VIDEO_FEED.capture()
        if video_frame:
            EMOTION_DETECTION.image = video_frame
            # draw the emotion on the frame
            cv.putText(video_frame.image, EMOTION_DETECTION.current_emotion, (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv.imshow('Video', video_frame.image)
        if cv.waitKey(1) & 0xFF == ord('q'):
            WORKER_MANAGER.stop_all_workers()
            break
