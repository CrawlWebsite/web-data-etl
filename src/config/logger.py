import logging
import coloredlogs
import sys

class ColoredFormatter(logging.Formatter):
    green = "\x1b[32;20m"
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s - %(levelname)s [%(name)s] %(message)s"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: green + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

class LoggerCustom:
    format = "%(asctime)s %(levelname)s [%(context)s] %(message)s"

    def __init__(self, context):
        self.context = context
        self.logger = logging.getLogger(context)
        self.logger.setLevel(logging.DEBUG)

        logging.setLogRecordFactory(logging.LogRecord)

        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.DEBUG)

        formatter = ColoredFormatter(fmt=self.format,
                                     datefmt=None)

        ch.setFormatter(formatter)

        self.logger.addHandler(ch)

    def info(self, message):
        self.logger.info(message)

    def warn(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)