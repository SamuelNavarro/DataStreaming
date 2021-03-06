"""Contains functionality related to Weather"""
import logging
import json

logger = logging.getLogger(__name__)


class Weather:
    """Defines the Weather model"""

    def __init__(self):
        """Creates the weather model"""
        self.temperature = 70.0
        self.status = "sunny"

    def process_message(self, message):
        """Handles incoming weather data"""
        logger.info("process msg in weather process_message")
        try:
            val = json.loads(message.value())
            self.temperature = val["temperature"]
            self.status = val["status"]
            logger.info(f"Weather temp: {self.temperature}, status: {self.status}")
        except Exception as e:
            logger.fatal(f"unable to process weather message: {message}, {e}")
