"""
Mock ST7789 class for testing purposes on Windows
Author: Benjamin Dodd (1901386)
"""
class ST7789(object):

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

    def display(self, image):
        """
        Display an image on the ST7789.
        """
        return
