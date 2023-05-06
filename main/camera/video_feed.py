"""
Video Feed Singleton class using OpenCV
Author: Benjamin Dodd (1901386)
"""

import threading
import cv2 as cv

from main.camera import LOGGER

CAMERA_FPS = 15
CAMERA_WIDTH = 480
CAMERA_HEIGHT = 240

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

class VideoFeed:
    """
    Provides access to the video feed
    """

    _feed = cv.VideoCapture(0)
    _lock = threading.Lock()
    _cache: VideoFrame = None
    _initialized = False
    _instance = None
    _instance_lock = threading.Lock()

    def __new__(cls):
        if not VideoFeed._instance:
            with VideoFeed._instance_lock:
                if not VideoFeed._instance:
                    VideoFeed._instance = super(VideoFeed, cls).__new__(cls)
        return VideoFeed._instance


    def __init__(self):
        if not VideoFeed._initialized:
            self._feed.set(cv.CAP_PROP_FPS, CAMERA_FPS)
            self._feed.set(cv.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
            self._feed.set(cv.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
            if not self._feed.isOpened():
                LOGGER.error("Failed to open video feed")
                raise RuntimeError("Failed to open video feed")
            VideoFeed._initialized = True

    def __del__(self):
        self._feed.release()
        VideoFeed._initialized = False

    def capture(self):
        """
        Captures a frame from the video feed

        Returns:
            VideoFrame: Frame from the video feed
        """
        with self._lock:
            if self._feed.isOpened():
                success, frame_capture = self._feed.read()
                if success:
                    frame_capture = VideoFrame(frame_capture)
                    self._cache = frame_capture
                    return frame_capture

                # If we failed to capture a frame, return the last frame we captured
                if self._cache:
                    return self._cache

                LOGGER.error("Failed to capture frame")
