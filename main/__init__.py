import logging
import sys
import os

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG,
    format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
    datefmt="%d/%m/%Y %H:%M:%S")
LOGGER = logging.getLogger(__name__)

IS_RASPBERRY_PI = os.uname()[4][:3] == 'arm'
