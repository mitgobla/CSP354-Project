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


MP_DRAWING = mp.solutions.drawing_utils
MP_DRAWING_STYLES = mp.solutions.drawing_styles
MP_HANDS = mp.solutions.hands

class GestureDetection(threading.Thread):
    """Thread for detecting gestures in a frame
    """
    def __init__(self, frame: VideoFrame):
        super().__init__()
        self.__image = frame.to_pillow()

    def run(self):
        with MP_HANDS.Hands(
                model_complexity=0,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5) as hands:
            self.__image.flags.writeable = False
            results = hands.process(self.__image)
            self.__image.flags.writeable = True

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

if __name__ == '__main__':
    from .video_feed import VIDEO_FEED

    while True:
        video_frame = VIDEO_FEED.capture()
        if video_frame:
            gesture_detection = GestureDetection(video_frame)
            gesture_detection.start()
            gesture_detection.join()
            # draw the gesture on the frame
            current_gesture = GESTURE_REPOSITORY.current_gesture
            LOGGER.debug("Current gesture: %s", current_gesture)
            cv.putText(video_frame.image, str(current_gesture), (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv.imshow('Video', video_frame.image)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break
