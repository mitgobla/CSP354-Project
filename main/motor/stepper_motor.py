"""
Driver class for stepper motors.

Portions of this code were produced from the examples in the LABISTS Starter Kit User Manual:
LABISTS, “Raspberry Pi Starter Kit Tutorial,” [Online]. Available: https://labists.com/pages/starter-kit-tutorial. [Accessed 12 February 2023].

Author: Benjamin Dodd (1901386)
"""

import time
from enum import Enum

from main.motor import LOGGER

try:
    import RPi.GPIO as GPIO
except ImportError:
    from main.util.mock_gpio import MockGPIO as GPIO

from main.util.storable_type import StorableType
from main.threading.worker_manager import WorkerManager
from main.threading.worker_thread import Worker

CLOCKWISE = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]

class StepperMotorDirection(Enum):
    """Enum for the direction of a stepper motor."""
    TURN_CLOCKWISE = 1
    TURN_ANTICLOCKWISE = 2

class StepperMotor:
    """
    Driver class for stepper motors.
    """

    def __init__(self, in1: int = 11, in2: int = 13, in3: int = 15, in4: int = 16, speed: float = 0.0005):
        """Create a new instance of the StepperMotor class."""
        self.in1 = in1
        self.in2 = in2
        self.in3 = in3
        self.in4 = in4
        self.speed = speed if speed >= 0.0005 else 0.0005
        self.steps = StorableType("stepper_motor_steps", 0)

        self.worker = None
        self.setup()
        self.rotate_to(0)

    def setup(self):
        """
        Set up the GPIO pins for the stepper motor.
        """
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.in1, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.in2, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.in3, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.in4, GPIO.OUT, initial=GPIO.LOW)

    def rotate_to(self, degrees: int):
        """Rotate the stepper motor to a specific angle.

        Args:
            degrees (int): Angle to rotate to.
        """
        if self.worker is not None:
            self.worker.stop()

        steps = int((degrees / 360) * 512)
        if steps < 0:
            steps = abs(steps)
            direction = StepperMotorDirection.TURN_ANTICLOCKWISE
        else:
            direction = StepperMotorDirection.TURN_CLOCKWISE
        self.worker = StepperMotorWorker(self, direction, steps)
        self.worker.start()
        LOGGER.debug("Stepper motor rotated to %d degrees", degrees)

    def step_clockwise(self, steps: int = 1):
        """Step the stepper motor clockwise.

        Args:
            steps (int, optional): Number of steps to perform. Defaults to 1.
        """
        if self.worker is not None:
            self.worker.stop()

        self.worker = StepperMotorWorker(self, StepperMotorDirection.TURN_CLOCKWISE, steps)
        self.worker.start()
        LOGGER.debug("Stepper motor stepped clockwise %d steps", steps)

    def step_anticlockwise(self, steps: int = 1):
        """Step the stepper motor anticlockwise.

        Args:
            steps (int, optional): Number of steps to perform. Defaults to 1.
        """
        if self.worker is not None:
            self.worker.stop()

        self.worker = StepperMotorWorker(self, StepperMotorDirection.TURN_ANTICLOCKWISE, steps)
        self.worker.start()
        LOGGER.debug("Stepper motor stepped anticlockwise %d steps", steps)

class StepperMotorWorker(Worker):
    """
    Worker thread for the stepper motor.
    """
    running = False

    def __init__(self, motor: StepperMotor, direction: StepperMotorDirection, steps: int):
        """Create a new instance of the StepperMotorWorker class."""
        super().__init__()
        self.motor = motor
        self.direction = direction
        self.steps = steps

    def clockwise(self):
        """
        Step the stepper motor clockwise.
        """
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
        """
        Step the stepper motor anticlockwise.
        """
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


if __name__ == "__main__":
    WORKER_MANAGER = WorkerManager()

    STEPPER_MOTOR = StepperMotor(11, 13, 15, 16)
    STEPPER_MOTOR.step_clockwise(10)
    time.sleep(3)
    STEPPER_MOTOR.step_anticlockwise(10)
    time.sleep(3)
    WORKER_MANAGER.stop_all_workers()
