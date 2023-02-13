"""
Circular Displays Driver
Author: Benjamin Dodd (1901386)
"""

import time

from PIL import Image

from . import LOGGER

try:
    import ST7789
except ImportError:
    from ..util import mock_st77789 as ST7789

from ..util.singleton import Singleton

class Display(object):
    """
    Circular Display Driver
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

        self._display = ST7789.ST7789(
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

        # black background
        self.image = None
        self.clear()


    def display(self, image: Image):
        """
        Draws an image on the display
        """
        self.image = image
        self._display.display(image.resize((self.diameter, self.diameter)))

    def clear(self):
        """
        Clears the display
        """
        self.display(Image.new("RGB", (self.diameter, self.diameter), (0, 0, 0)))

class LeftDisplay(Display, Singleton):
    """
    Left Circular Display Driver
    """
    def __init__(self):
        super().__init__(diameter=240, rotation=0, port=0, cs_pin=1, dc_pin=9, backlight=19)

class RightDisplay(Display, Singleton):
    """
    Right Circular Display Driver
    """
    def __init__(self):
        super().__init__(diameter=240, rotation=180, port=0, cs_pin=0, dc_pin=9, backlight=18)

if __name__ == '__main__':
    RD = RightDisplay()
    LD = LeftDisplay()