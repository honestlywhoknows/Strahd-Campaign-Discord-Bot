import errno
import os

class Error(Exception):
    pass

def handle_error(error_code):
    error_message = os.strerror(error_code)
    if error_code == errno.ENOENT:
        raise Error("File not found")
    elif error_code == errno.EPERM:
        raise Error("Operation not permitted")
    else:
        raise Error(error_message)
