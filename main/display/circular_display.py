"""
Circular Displays Driver
Author: Benjamin Dodd (1901386)
"""

import threading

from PIL import Image
import cv2 as cv
import numpy as np

from . import LOGGER

try:
    import ST7789
    RASPI_LIB = True
except ImportError:
    from ..util import mock_st77789 as ST7789
    RASPI_LIB = False

from ..threading.worker_manager import WORKER_MANAGER
from ..threading.worker_thread import WorkerThread
from ..util.singleton import Singleton

class Display(object):
    """
    Circular Display Driver
    """

    class DisplayWorker(WorkerThread):

        def __init__(self, display: "Display"):
            super().__init__()
            self.display = display

        def work(self):
            if self.display.image is not None:
                if RASPI_LIB:
                    self.display.st7798.display(cv.resize(self.display.image, (self.display.diameter, self.display.diameter)))
                else:
                    self.display.st7798.display(self.display.image)

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

        self.__lock = threading.Lock()
        self.__image = None
        self.clear()

    @property
    def image(self):
        """Gets the image to be displayed on the display.

        Returns:
            Image: The image to be displayed on the display.
        """
        with self.__lock:
            return self.__image

    @image.setter
    def image(self, image: cv.Mat):
        """Sets the image to be displayed on the display.

        Args:
            image (Image): The image to be displayed on the display.
        """
        with self.__lock:
            self.__image = image
            worker = self.DisplayWorker(self)
            WORKER_MANAGER.add_thread(worker)

    def clear(self):
        """
        Clears the display
        """
        blank = Image.new("RGB", (self.diameter, self.diameter), (0, 0, 0))
        blank = cv.cvtColor(np.asarray(blank), cv.COLOR_RGB2BGR)
        self.image = blank

class LeftDisplay(Display, metaclass = Singleton):
    """
    Left Circular Display Driver
    """
    def __init__(self):
        super().__init__(diameter=240, rotation=0, port=0, cs_pin=1, dc_pin=9, backlight=19)

class RightDisplay(Display, metaclass = Singleton):
    """
    Right Circular Display Driver
    """
    def __init__(self):
        super().__init__(diameter=240, rotation=180, port=0, cs_pin=0, dc_pin=9, backlight=18)

if __name__ == '__main__':
    import time
    from ..camera.video_feed import VIDEO_FEED

    RD = RightDisplay()
    LD = LeftDisplay()


    while True:
        video_frame = VIDEO_FEED.capture()
        if video_frame:
            RD.image = video_frame.image
            LD.image = video_frame.image
        time.sleep(0.15)