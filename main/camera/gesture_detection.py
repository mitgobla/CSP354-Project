"""
Gesture detection using MediaPipe
Author: Benjamin Dodd (1901386)
"""

import threading

import cv2 as cv
import mediapipe as mp

from . import LOGGER

from .video_feed import VideoFrame

from ..threading.worker_manager import WorkerManager
from ..threading.worker_thread import WorkerThread


MP_DRAWING = mp.solutions.drawing_utils
MP_DRAWING_STYLES = mp.solutions.drawing_styles
MP_HANDS = mp.solutions.hands

class GestureDetection:
    """
    Class for detecting gestures in a frame
    """

    _lock = threading.Lock()
    _image = None
    _finger_count = 0

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
    def image(self, image: VideoFrame):
        """
        Set the image to analyse.
        """
        with self._lock:
            # Ignore if the worker is already running
            if self.worker is not None:
                if self.worker.is_running():
                    return

            self._image = image.to_pillow()
            self.worker = GestureDetectionWorker(self)
            self.worker_manager.add_worker(self.worker)

    @property
    def finger_count(self):
        """
        Get the finger count.
        """
        with self._lock:
            return self._finger_count

    @finger_count.setter
    def finger_count(self, finger_count: int):
        """
        Set the finger count.
        """
        with self._lock:
            self._finger_count = finger_count

class GestureDetectionWorker(WorkerThread):
    """
    Worker thread for the gesture detection.
    """
    _running = False

    def __init__(self, gesture_detection: GestureDetection):
        """Create a new instance of the GestureDetectionWorker class."""
        super().__init__()
        self.gesture_detection = gesture_detection

    def is_running(self):
        """
        Check if the worker thread is running.
        """
        return self._running

    def work(self):
        """
        Run the worker thread.
        """
        if self._running or self.gesture_detection.image is None:
            return

        self._running = True

        finger_count = 0
        with MP_HANDS.Hands(
            # model_complexity=0,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as hands:
            results = hands.process(self.gesture_detection.image)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    if hand_landmarks.landmark[MP_HANDS.HandLandmark.INDEX_FINGER_TIP].y < hand_landmarks.landmark[MP_HANDS.HandLandmark.INDEX_FINGER_DIP].y:
                        finger_count += 1

                    if hand_landmarks.landmark[MP_HANDS.HandLandmark.MIDDLE_FINGER_TIP].y < hand_landmarks.landmark[MP_HANDS.HandLandmark.MIDDLE_FINGER_DIP].y:
                        finger_count += 1

                    if hand_landmarks.landmark[MP_HANDS.HandLandmark.RING_FINGER_TIP].y < hand_landmarks.landmark[MP_HANDS.HandLandmark.RING_FINGER_DIP].y:
                        finger_count += 1

                    if hand_landmarks.landmark[MP_HANDS.HandLandmark.PINKY_TIP].y < hand_landmarks.landmark[MP_HANDS.HandLandmark.PINKY_DIP].y:
                        finger_count += 1

        self.gesture_detection.finger_count = finger_count
        self._running = False

if __name__ == "__main__":
    from .video_feed import VideoFeed

    VIDEO_FEED = VideoFeed()
    GESTURE_DETECTION = GestureDetection()

    while True:
        video_frame = VIDEO_FEED.capture()
        if video_frame:
            GESTURE_DETECTION.image = video_frame
            cv.putText(video_frame.image, str(GESTURE_DETECTION.finger_count), (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv.LINE_AA)
            cv.imshow("Gesture Detection", video_frame.image)
        if cv.waitKey(1) & 0xFF == ord('q'):
            GESTURE_DETECTION.worker_manager.stop_all_workers()
            break
