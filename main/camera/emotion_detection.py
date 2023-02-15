"""
Emotion detection using OpenCV and SkiKit
Author: Benjamin Dodd (1901386)
"""

import threading

import cv2 as cv
from deepface import DeepFace

from . import LOGGER

from .emotion_repository import EMOTION_REPOSITORY
from .video_feed import VideoFrame

class EmotionDetection(threading.Thread):
    """Thread for detecting emotions in a frame
    """
    def __init__(self, frame: VideoFrame):
        super().__init__()
        self.__image = frame.image

    def run(self):
        try:
            face_analysis = DeepFace.analyze(self.__image, actions = ['emotion'], enforce_detection=False, silent = True)[0]
            dominant_emotion = face_analysis['dominant_emotion']
            EMOTION_REPOSITORY.current_emotion = dominant_emotion
        except cv.error:
            return

if __name__ == "__main__":
    from .video_feed import VIDEO_FEED

    while True:
        video_frame = VIDEO_FEED.capture()
        if video_frame:
            emotion_detection = EmotionDetection(video_frame)
            emotion_detection.start()
            emotion_detection.join()
            # draw the emotion on the frame
            current_emotion = EMOTION_REPOSITORY.current_emotion
            cv.putText(video_frame.image, EMOTION_REPOSITORY.current_emotion, (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv.imshow('Video', video_frame.image)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
