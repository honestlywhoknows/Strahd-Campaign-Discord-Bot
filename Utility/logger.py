import logging
from logging.handlers import RotatingFileHandler
from Utility.config import Config

config = Config()

def setup_logger(test):
    # Create a logger with the lowest level; debug messages will be logged here
    logger = logging.getLogger('discord')
    logger.setLevel(logging.DEBUG if test else logging.INFO)

    # Formatter to output time, level, and message
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # File handler for debug.log: will log debug and higher levels
    debug_handler = RotatingFileHandler('debug.log', maxBytes=10*1024*1024, backupCount=10)
    debug_handler.setLevel(logging.DEBUG)
    debug_handler.setFormatter(formatter)

    # File handler for prod.log: will log info and higher levels
    prod_handler = RotatingFileHandler('prod.log', maxBytes=5*1024*1024, backupCount=5)
    prod_handler.setLevel(logging.INFO)
    prod_handler.setFormatter(formatter)

    # Adding handlers to the logger
    if test:
        logger.addHandler(debug_handler)
    else:
        logger.addHandler(prod_handler)

    return logger

# Initialize the logger
logger = setup_logger(config.is_test_mode())
