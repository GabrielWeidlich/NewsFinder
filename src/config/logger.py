import logging
import sys

from config import settings

# Create a logger
logger = logging.getLogger(settings.PROJECT_NAME)

# Configure logger
logger.setLevel(settings.LOG_LEVEL.upper())

# Create a handler
handler = logging.StreamHandler(sys.stdout)

# Create a formatter and add it to the handler
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(handler)