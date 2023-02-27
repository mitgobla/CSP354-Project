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

class VideoFeed(metaclass = Singleton):
    """Singleton class that provides access to the video feed

    Raises:
        RuntimeError: Failed to open video feed, or failed to capture frame
    """

    __feed = cv.VideoCapture(0)
    __lock = threading.Lock()
    __cache: VideoFrame = None

    def __init__(self):
        self.__feed.set(cv.CAP_PROP_FPS, 15)
        self.__feed.set(cv.CAP_PROP_FRAME_WIDTH, 480)
        self.__feed.set(cv.CAP_PROP_FRAME_HEIGHT, 240)
        if not self.__feed.isOpened():
            LOGGER.error("Failed to open video feed")
            raise RuntimeError("Failed to open video feed")

    def __del__(self):
        self.__feed.release()

    def capture(self) -> VideoFrame:
        """
        Captures a frame from the video feed

        Returns:
            VideoFrame: Frame from the video feed
        """
        with self.__lock:
            if self.__feed.isOpened():
                success, frame_capture = self.__feed.read()
                if success:
                    frame_capture = VideoFrame(frame_capture)
                    self.__cache = frame_capture
                    return frame_capture

                # If we failed to capture a frame, return the last frame we captured
                if self.__cache:
                    return self.__cache

                LOGGER.error("Failed to capture frame")
                raise RuntimeError("Failed to capture frame")

VIDEO_FEED = VideoFeed()

if __name__ == "__main__":
    while True:
        frame = VIDEO_FEED.capture()
        cv.imshow("Video", frame.image)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    cv.destroyAllWindows()
    del VIDEO_FEED
