"""
Video Feed Singleton class using OpenCV
Author: Benjamin Dodd (1901386)
"""

import threading
import cv2 as cv

from . import LOGGER

from ..util.singleton import Singleton

class VideoFrame:
    """Video Frame class, holds an image from the video feed

    Args:
        frame (cv.Mat): Frame from the video feed
    """
    def __init__(self, frame: cv.Mat):
        self.image = frame

    def __str__(self):
        return f"VideoFrame({self.image.shape})"

    def __repr__(self):
        return self.__str__()

    def to_pillow(self):
        """Returns a RGB representation of the frame that can be used by PIL library

        Returns:
            cv.Mat: RGB representation of the frame
        """
        return cv.cvtColor(self.image, cv.COLOR_BGR2RGB)

class VideoFeed(Singleton):

    __feed = cv.VideoCapture(0)
    __lock = threading.Lock()
    __cache = None

    def __init__(self):
        if not self.__feed.isOpened():
            LOGGER.error("Failed to open video feed")
            raise RuntimeError("Failed to open video feed")

    def __del__(self):
        self.__feed.release()

    def capture(self):
        """
        Captures a frame from the video feed
        """
        with self.__lock:
            with self.__feed.isOpened():
                ret, frame = self.__feed.read()
                if ret:
                    self.__cache = frame
                    return frame
                else:
                    if self.__cache:
                        return self.__cache
                    else:
                        LOGGER.error("Failed to capture frame")
                        raise RuntimeError("Failed to capture frame")