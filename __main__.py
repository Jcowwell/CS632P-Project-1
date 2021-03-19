import logging
from sys import stdout
from test import run
from constants import LOG_FORMAT, LOG_DATE_FORMAT


# NOTE: - Formatter
formatter = logging.Formatter(fmt=LOG_FORMAT, datefmt=LOG_DATE_FORMAT)

# NOTE: - Logger Configuration
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def log_file_config():
    # NOTE:: - Log File Configuration
    # NOTE: - Set Up Handler
    output_file_handler = logging.FileHandler("test.log")

    # NOTE: - Add Formatter
    output_file_handler.setFormatter(formatter)

    # NOTE: - Add Handlers
    logger.addHandler(output_file_handler)

if __name__ == '__main__':
    log_file_config()
    logger.debug("In Main File")
    logger.info('Started')
    run()
    logger.info('Finished')
