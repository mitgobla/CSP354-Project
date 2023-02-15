"""
Mock GPIO class for testing purposes on Windows
Author: Benjamin Dodd (1901386)
"""

from . import LOGGER

class MockGPIO:
    """
    Mock GPIO class for testing purposes on Windows
    """
    BOARD = "BOARD"
    BCM = "BCM"
    OUT = "OUT"
    LOW = "LOW"
    HIGH = "HIGH"
    IN = "IN"

    @classmethod
    def setwarnings(cls, enabled: bool):
        """Enable or disable GPIO warnings.

        Args:
            enabled (bool): True to enable warnings, False to disable.
        """
        LOGGER.debug("MockGPIO.setWarnings(%s)", enabled)

    @classmethod
    def setmode(cls, mode: str):
        """Set the pin numbering mode.

        Args:
            mode (str): The pin numbering mode. Must be either MockGPIO.BOARD or MockGPIO.BCM.
        """
        LOGGER.debug("MockGPIO.setmode(%s)", mode)

    @classmethod
    def setup(cls, pin: int, mode: str, initial: str = None):
        """Set up a GPIO pin.

        Args:
            pin (int): The pin number.
            mode (str): The pin mode. Must be either MockGPIO.IN or MockGPIO.OUT.
            initial (str, optional): Initial state of the pin. Must be either MockGPIO.LOW or MockGPIO.HIGH. Defaults to None.
        """
        LOGGER.debug("MockGPIO.setup(%s, %s, %s)", pin, mode, initial)

    @classmethod
    def output(cls, pin: int, value: str):
        """Set the state of a GPIO pin.

        Args:
            pin (int): The pin number.
            value (str): The state to set the pin to. Must be either MockGPIO.LOW or MockGPIO.HIGH.
        """
        LOGGER.debug("MockGPIO.output(%s, %s)", pin, value)

    @classmethod
    def input(cls, pin: int) -> int:
        """Read the state of a GPIO pin.

        Args:
            pin (int): The pin number.

        Returns:
            int: The state of the pin. 0 for MockGPIO.LOW, 1 for MockGPIO.HIGH.
        """
        LOGGER.debug("MockGPIO.input(%s)", pin)
        return 0
