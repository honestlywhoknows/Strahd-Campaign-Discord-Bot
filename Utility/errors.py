import errno
import os
from Utility.logger import logger

class Error(Exception):
    pass

def handle_error(error_code):
    error_message = os.strerror(error_code)
    logger.error(error_message)
    if error_code == errno.ENOENT:
        raise Error("File not found")
    elif error_code == errno.EPERM:
        raise Error("Operation not permitted")
    else:
        raise Error(error_message)
