"""
Driver class for stepper motors.
Author: Benjamin Dodd (1901386)
"""

import time
from enum import Enum

from . import LOGGER

try:
    import RPi.GPIO as GPIO
except ImportError:
    from ..util.mock_gpio import MockGPIO as GPIO

from ..util.singleton import Singleton
from ..util.storable_type import StorableType
from ..threading.worker_manager import WORKER_MANAGER
from ..threading.worker_thread import WorkerThread

CLOCKWISE = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]

class StepperMotorDirection(Enum):
    """Enum for the direction of a stepper motor."""
    TURN_CLOCKWISE = 1
    TURN_ANTICLOCKWISE = 2
class StepperMotor(metaclass = Singleton):
    """
    Driver class for stepper motors.
    """

    class StepperMotorWorker(WorkerThread):
        """
        Worker thread for the stepper motor.
        """
        running = False

        def __init__(self, motor: "StepperMotor", direction: StepperMotorDirection, steps: int):
            """Create a new instance of the StepperMotorWorker class."""
            super().__init__()
            self.motor = motor
            self.direction = direction
            self.steps = steps

        def clockwise(self):
            for _ in range(self.steps):
                for step in CLOCKWISE:
                    GPIO.output(self.motor.in1, step[0])
                    time.sleep(self.motor.speed)
                    GPIO.output(self.motor.in2, step[1])
                    time.sleep(self.motor.speed)
                    GPIO.output(self.motor.in3, step[2])
                    time.sleep(self.motor.speed)
                    GPIO.output(self.motor.in4, step[3])
                    time.sleep(self.motor.speed)
                self.motor.steps.value += 1

        def anticlockwise(self):
            for _ in range(self.steps):
                for step in CLOCKWISE[::-1]:
                    GPIO.output(self.motor.in4, step[0])
                    time.sleep(self.motor.speed)
                    GPIO.output(self.motor.in3, step[1])
                    time.sleep(self.motor.speed)
                    GPIO.output(self.motor.in2, step[2])
                    time.sleep(self.motor.speed)
                    GPIO.output(self.motor.in1, step[3])
                    time.sleep(self.motor.speed)
                self.motor.steps.value -= 1

        def work(self):
            """
            Run the worker thread.
            """
            if self.running:
                return
            self.running = True
            if self.direction == StepperMotorDirection.TURN_CLOCKWISE:
                self.clockwise()
            elif self.direction == StepperMotorDirection.TURN_ANTICLOCKWISE:
                self.anticlockwise()
            self.running = False

    def __init__(self, in1: int, in2: int, in3: int, in4: int, speed: float = 0.0005):
        """Create a new instance of the StepperMotor class."""
        self.in1 = in1
        self.in2 = in2
        self.in3 = in3
        self.in4 = in4
        self.speed = speed if speed >= 0.0005 else 0.0005
        self.steps = StorableType("stepper_motor_steps", 0)
        self.setup()

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
        worker = StepperMotor.StepperMotorWorker(self, StepperMotorDirection.TURN_CLOCKWISE, steps)
        WORKER_MANAGER.add_thread(worker)
        LOGGER.debug("Stepper motor stepped clockwise %d steps", steps)

    def step_anticlockwise(self, steps: int = 1):
        """Step the stepper motor anticlockwise.

        Args:
            steps (int, optional): Number of steps to perform. Defaults to 1.
        """
        worker = StepperMotor.StepperMotorWorker(self, StepperMotorDirection.TURN_ANTICLOCKWISE, steps)
        WORKER_MANAGER.add_thread(worker)
        LOGGER.debug("Stepper motor stepped anticlockwise %d steps", steps)

STEPPER_MOTOR = StepperMotor(11, 13, 15, 16)

if __name__ == "__main__":
    STEPPER_MOTOR.step_clockwise(10)
    time.sleep(3)
    STEPPER_MOTOR.step_anticlockwise(10)