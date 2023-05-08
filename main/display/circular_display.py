"""
Circular Displays Driver
Author: Benjamin Dodd (1901386)
"""

import threading

from PIL import Image
import cv2 as cv
import numpy as np

from main.display import LOGGER

try:
    import ST7789
except ImportError:
    from main.util import mock_st77789 as ST7789

from main.threading.worker_manager import WorkerManager
from main.threading.worker_thread import Worker

class Display(object):
    """
    Circular Display Driver

    Portions of this code were produced based on a forums post by user 'MeckerZiege' on the Pimonori forums:
    MeckerZiege, “Pimoroni Forums,” March 2021. [Online]. Available: https://forums.pimoroni.com/t/two-1-3-spi-colour-lcd-240x240-on-one-pi/16737/7. [Accessed 12 February 2023].
    """

    def __init__(self, diameter: int, rotation: int, port: int, cs_pin: int, dc_pin: int, backlight: int):
        self.diameter = diameter
        self.rotation = rotation
        self.port = port
        self.cs_pin = cs_pin
        self.dc_pin = dc_pin
        self.backlight = backlight
        self.spi_speed_hz = 32 * 1000 * 1000
        self.offset_left = 40
        self.offset_top = 0

        self.st7798 = ST7789.ST7789(
            height=self.diameter,
            rotation=self.rotation,
            port=self.port,
            cs=self.cs_pin,
            dc=self.dc_pin,
            backlight=self.backlight,
            spi_speed_hz=self.spi_speed_hz,
            offset_left=self.offset_left,
            offset_top=self.offset_top
        )

        self.worker = None

        self._lock = threading.Lock()
        self._image = None
        self.clear()

    @property
    def image(self):
        """Gets the image to be displayed on the display.

        Returns:
            Image: The image to be displayed on the display.
        """
        with self._lock:
            return self._image

    @image.setter
    def image(self, image: cv.Mat):
        """Sets the image to be displayed on the display.

        Args:
            image (Image): The image to be displayed on the display.
        """
        with self._lock:
            self._image = image
            if self.worker is not None:
                if self.worker.is_running():
                    return
            self.worker = DisplayWorker(self)
            self.worker.start()

    def display_number(self, number: int, colour: tuple = (255, 255, 255)):
        """Displays a number on the display.

        Args:
            number (int): The number to display.
        """
        text = str(number)
        text_size = cv.getTextSize(text, cv.FONT_HERSHEY_SIMPLEX, 3, 3)
        text_x = (self.diameter - text_size[0][0]) // 2
        text_y = (self.diameter + text_size[0][1]) // 2
        blank = Image.new("RGB", (self.diameter, self.diameter), (0, 0, 0))
        blank = cv.cvtColor(np.asarray(blank), cv.COLOR_RGB2BGR)
        self.image = cv.putText(blank, text, (text_x, text_y), cv.FONT_HERSHEY_SIMPLEX, 3, colour, 3, cv.LINE_AA)

    def display_text(self, text: str, colour: tuple = (255, 255, 255)):
        """Displays text on the display.

        Args:
            text (str): The text to display.
        """
        text_size = cv.getTextSize(text, cv.FONT_HERSHEY_SIMPLEX, 2, 2)
        text_x = (self.diameter - text_size[0][0]) // 2
        text_y = (self.diameter + text_size[0][1]) // 2
        blank = Image.new("RGB", (self.diameter, self.diameter), (0, 0, 0))
        blank = cv.cvtColor(np.asarray(blank), cv.COLOR_RGB2BGR)
        self.image = cv.putText(blank, text, (text_x, text_y), cv.FONT_HERSHEY_SIMPLEX, 2, colour, 2, cv.LINE_AA)

    def clear(self):
        """
        Clears the display
        """
        blank = Image.new("RGB", (self.diameter, self.diameter), (0, 0, 0))
        blank = cv.cvtColor(np.asarray(blank), cv.COLOR_RGB2BGR)
        self.image = blank

class DisplayWorker(Worker):

    def __init__(self, display: Display):
        super().__init__()
        self.running = True
        self.display = display

    def is_running(self):
        """
        Returns whether the worker is running or not.
        """
        return self.running

    def work(self):
        if self.display.image is not None:
                self.display.st7798.display(cv.resize(self.display.image, (self.display.diameter, self.display.diameter)))
        self.running = False

class LeftDisplay(Display):
    """
    Left Circular Display Driver
    """

    _instance = None
    _instance_lock = threading.Lock()
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            with cls._instance_lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            super().__init__(diameter=240, rotation=90, port=0, cs_pin=1, dc_pin=9, backlight=19)
            LOGGER.debug("Left Display created")

class RightDisplay(Display):
    """
    Right Circular Display Driver
    """
    _instance = None
    _instance_lock = threading.Lock()
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            with cls._instance_lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            super().__init__(diameter=240, rotation=90, port=0, cs_pin=0, dc_pin=9, backlight=18)
            LOGGER.debug("Right Display created")


if __name__ == '__main__':
    from ..camera.video_feed import VideoFeed

    WORKER_MANAGER = WorkerManager()

    RIGHT_DISPLAY = RightDisplay()
    LEFT_DISPLAY = LeftDisplay()
    VIDEO_FEED = VideoFeed()

    while True:
        video_frame = VIDEO_FEED.capture()
        if video_frame:
            RIGHT_DISPLAY.image = video_frame.image
            LEFT_DISPLAY.image = cv.flip(video_frame.image, 1)
            cv.imshow("Video Feed", video_frame.image)
            cv.imshow("Right Display", RIGHT_DISPLAY.image)
            cv.imshow("Left Display", LEFT_DISPLAY.image)
        if cv.waitKey(1) & 0xFF == ord('q'):
            WORKER_MANAGER.worker_manager.stop_all_workers()
            break
