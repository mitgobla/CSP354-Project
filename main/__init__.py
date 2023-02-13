import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG,
    format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
    datefmt="%d/%m/%Y %H:%M:%S")
LOGGER = logging.getLogger(__name__)
