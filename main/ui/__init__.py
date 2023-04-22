import os
import logging

LOGGER = logging.getLogger(__name__)

RESOURCE_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "res", "ui")
LOGGER.debug("Resource path: %s", RESOURCE_PATH)
