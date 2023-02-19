"""
Mock ST7789 class for testing purposes on Windows
Author: Benjamin Dodd (1901386)
"""
import cv2 as cv
from PIL import Image
import numpy as np
import threading
import time

from . import LOGGER

from ..threading.worker_manager import WORKER_MANAGER
from ..threading.worker_thread import WorkerThread
from ..camera.video_feed import VideoFrame

class ST7789(object):

    __id = 0

    class ST7789Worker(WorkerThread):
        """
        Worker thread for the mock ST7789.
        """
        running = False

        def __init__(self, st7789: "ST7789"):
            """Create a new instance of the ST7789Worker class."""
            super().__init__()
            self.st7789 = st7789

        def work(self):
            """
            Run the worker thread.
            """
            while True:
                if self.st7789.image is None:
                    # time.sleep(0.1)
                    continue
                new_image = np.array(self.st7789.image)
                cv.imshow("ST7789-"+str(self.st7789.id), new_image)
                if cv.waitKey(1) & 0xFF == ord('q'):
                    break

    def __init__(self, height, rotation, port, cs, dc, backlight, spi_speed_hz, offset_left, offset_top):
        self.height = height
        self.rotation = rotation
        self.port = port
        self.cs = cs
        self.dc = dc
        self.backlight = backlight
        self.spi_speed_hz = spi_speed_hz
        self.offset_left = offset_left
        self.offset_top = offset_top

        self.id = ST7789.__id
        ST7789.__id += 1

        self.__lock = threading.Lock()
        self.__image = None

        worker = self.ST7789Worker(self)
        WORKER_MANAGER.add_thread(worker)

        LOGGER.debug("Mock ST7789 initialised")

    def display(self, image):
        with self.__lock:
            self.__image = image

    @property
    def image(self):
        with self.__lock:
            return self.__image
