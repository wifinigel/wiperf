'''
A very simple file logging function based on Python native logging ,using
a rotating file handle to maintain file sizes
'''
from __future__ import print_function
import logging
import time
from logging.handlers import RotatingFileHandler


def FileLogger(log_file):
    '''
    A class to perform very simple logging to a named file. Any non-recoverable
    errors are written to stdout (e.g. can't open file)
    '''

    logger = logging.getLogger("Probe_Log")
    logger.setLevel(logging.INFO)

    # add a rotating handler
    handler = RotatingFileHandler(log_file, maxBytes=521000, backupCount=10)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
