"""
Video Feed Singleton class using OpenCV
Author: Benjamin Dodd (1901386)
"""

import threading
import cv2 as cv

from . import LOGGER

from ..util.singleton import Singleton

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