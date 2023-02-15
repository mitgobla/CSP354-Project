"""
Driver class for stepper motors.
Author: Benjamin Dodd (1901386)
"""

import time

from . import LOGGER

try:
    import RPi.GPIO as GPIO
except ImportError:
    from ..util.mock_gpio import MockGPIO as GPIO

from ..util.singleton import Singleton

CLOCKWISE = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]

class StepperMotor(Singleton):
    """
    Driver class for stepper motors.
    """
    __instance = None

    def __new__(cls, in1: int, in2: int, in3: int, in4: int, speed: float = 0.0005):
        """Create a new instance of the StepperMotor class."""
        if cls.__instance is None:
            cls.__instance = super(StepperMotor, cls).__new__(cls)
            cls.in1 = in1
            cls.in2 = in2
            cls.in3 = in3
            cls.in4 = in4
            cls.speed = speed if speed >= 0.0005 else 0.0005
            cls.setup(cls)
        return cls.__instance

    def setup(self):
        """
        Set up the GPIO pins for the stepper motor.
        """
        GPIO.setwarnings(False)
        # TODO: Change to BCM mode
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.in1, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.in2, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.in3, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.in4, GPIO.OUT, initial=GPIO.LOW)

    def step_clockwise(self, steps: int = 1):
        """Step the stepper motor clockwise.

        Args:
            steps (int, optional): Number of steps to perform. Defaults to 1.
        """
        for _ in range(steps):
            for step in CLOCKWISE:
                GPIO.output(self.in1, step[0])
                time.sleep(self.speed)
                GPIO.output(self.in2, step[1])
                time.sleep(self.speed)
                GPIO.output(self.in3, step[2])
                time.sleep(self.speed)
                GPIO.output(self.in4, step[3])
                time.sleep(self.speed)
        LOGGER.debug("Stepper motor stepped clockwise %d steps", steps)

    def step_anticlockwise(self, steps: int = 1):
        """Step the stepper motor anticlockwise.

        Args:
            steps (int, optional): Number of steps to perform. Defaults to 1.
        """
        for _ in range(steps):
            for step in CLOCKWISE[::-1]:
                GPIO.output(self.in4, step[0])
                time.sleep(self.speed)
                GPIO.output(self.in3, step[1])
                time.sleep(self.speed)
                GPIO.output(self.in2, step[2])
                time.sleep(self.speed)
                GPIO.output(self.in1, step[3])
                time.sleep(self.speed)
        LOGGER.debug("Stepper motor stepped anticlockwise %d steps", steps)

STEPPER_MOTOR = StepperMotor(11, 13, 15, 16)

if __name__ == "__main__":
    STEPPER_MOTOR.step_clockwise(10)
    STEPPER_MOTOR.step_anticlockwise(10)