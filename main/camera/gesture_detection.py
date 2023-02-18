"""
Gesture detection using MediaPipe
Author: Benjamin Dodd (1901386)
"""

import threading

import cv2 as cv
import mediapipe as mp

from . import LOGGER

from .gesture_repository import GESTURE_REPOSITORY
from .video_feed import VideoFrame

from ..threading.worker_manager import WORKER_MANAGER
from ..threading.worker_thread import WorkerThread
from ..util.singleton import Singleton


MP_DRAWING = mp.solutions.drawing_utils
MP_DRAWING_STYLES = mp.solutions.drawing_styles
MP_HANDS = mp.solutions.hands

class GestureDetection(metaclass=Singleton):
    """
    Class for detecting gestures in a frame
    """

    class GestureDetectionWorker(WorkerThread):
        """
        Worker thread for the gesture detection.
        """
        running = False

        def __init__(self, gesture_detection: "GestureDetection"):
            """Create a new instance of the GestureDetectionWorker class."""
            super().__init__()
            self.gesture_detection = gesture_detection

        def work(self):
            """
            Run the worker thread.
            """
            if self.running or self.gesture_detection.image is None:
                return

            with MP_HANDS.Hands(
                model_complexity=0,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5) as hands:
                results = hands.process(self.gesture_detection.image)

                finger_count = 0
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

                GESTURE_REPOSITORY.current_gesture = finger_count


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
    def image(self, image: VideoFrame):
        """
        Set the image to analyse.
        """
        with self.__lock:
            self.__image = image.to_pillow()
            worker = self.GestureDetectionWorker(self)
            WORKER_MANAGER.add_thread(worker)

GESTURE_DETECTION = GestureDetection()

if __name__ == '__main__':
    from .video_feed import VIDEO_FEED

    while True:
        video_frame = VIDEO_FEED.capture()
        if video_frame:
            GESTURE_DETECTION.image = video_frame
            # draw the gesture on the frame
            current_gesture = GESTURE_REPOSITORY.current_gesture
            LOGGER.debug("Current gesture: %s", current_gesture)
            cv.putText(video_frame.image, str(current_gesture), (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv.imshow('Video', video_frame.image)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break
