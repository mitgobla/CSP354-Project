# CSP354 Project

Author: [Benjamin Dodd (1901386)](https://www.github.com/mitgobla)

## Description

Software implementation of the soft-toy interactive robot.

## Setup

**Note:** This project requires specific hardware to run.

1. Ensure Python 3.7 is installed on your Raspberry Pi.
2. Ensure `run.sh` is executable by running `chmod +x raspberry_pi.sh`.
3. Run `./run.sh` to execute the program.

To try specific modules, run: `python3 -m main.<module_parent>.<module_name>` where `<module_parent>` and `<module_name>` are listed below.

### Modules

- `display.circular_display` - Displays the video feed onto both screens.
- `motor.stepper_motor` - Moves the stepper motor.
- `camera.emotion_detection` - Detects emotions from the video feed.
- `camera.gesture_detection` - Detects number of fingers shown from the video feed.
- `threading.worker_thread` - Runs a worker thread.

## Demo

### Menu navigation

![Menu navigation](docs/menu.gif)

### Clock Activity

![Clock activity](docs/clock.gif)

### Emotion Reaction Activity

![Emotion reaction activity](docs/emotion.gif)

### Number guessing Activity

![Number guessing activity](docs/number.gif)

## Circuit Diagram

![Electronics layout](docs/circuit.svg)

### Hardware components

- [Raspberry Pi 4 Model B 4GB](https://www.raspberrypi.org/products/raspberry-pi-4-model-b/)
- 2x [1.3" 240x240 SPI Colour Round LCD Display](https://shop.pimoroni.com/products/1-3-spi-colour-round-lcd-240x240-breakout)
- [Push Button](https://labists.com/collections/accessories/products/electronics-projects-starter-kit-for-raspberry-pi-4-3-b-arduino)
- [Capacitive Touch Sensor](https://labists.com/collections/accessories/products/electronics-projects-starter-kit-for-raspberry-pi-4-3-b-arduino)
- [Raspberry Pi Camera](https://www.raspberrypi.org/products/camera-module-v2/)
- [Stepper Motor](https://labists.com/collections/accessories/products/electronics-projects-starter-kit-for-raspberry-pi-4-3-b-arduino)

- Custom wiring
- Custom 3D printed mounts for circular displays
