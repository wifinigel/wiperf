'''
A very simple syslog logging function based on Python native logging.
'''
from __future__ import print_function
import logging
import time
from logging.handlers import SysLogHandler

def SysLogger(syslog_host_address, syslog_udp_port=514):
    '''
    A class to perform very simple logging to syslog. Any non-recoverable
    errors are written to stdout (e.g. can't open file)
    '''

    logger = logging.getLogger("Syslog_Log")
    logger.setLevel(logging.INFO)
 
    # add a rotating handler
    handler = SysLogHandler(syslog_host_address, syslog_udp_port)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger
    

