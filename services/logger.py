import logging
import sys
from datetime import datetime
from services.path import root_path


class Logger:
    def __init__(self):
        self.__setup()
        self.logger = logging.getLogger()

    def __setup(self):
        logging.basicConfig(
            format='%(asctime)s | %(name)s | %(levelname)s | %(message)s',
            handlers=[
                logging.StreamHandler(sys.stdout),
            ]
        )

    def info(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)

    def exception(self, message):
        self.logger.exception(message)