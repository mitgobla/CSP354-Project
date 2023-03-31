import logging
import sys
import platform

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG,
    format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
    datefmt="%d/%m/%Y %H:%M:%S")
LOGGER = logging.getLogger(__name__)

IS_RASPBERRY_PI = platform.machine()[0:3] == 'arm'
