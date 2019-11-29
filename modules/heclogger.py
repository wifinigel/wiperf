'''
A class to perform logging to Splunk using the HTTP event logger (HEC).
'''
import logging
from splunk_hec_handler import SplunkHecHandler

def HecLogger(host, token, port, source, debug):
    '''
    A class to perform logging to Splunk using the HTTP event logger (HEC).
    '''
    logger = logging.getLogger('SplunkHecHandler')
    logger.setLevel(logging.INFO)

    # If using self-signed certificate, set ssl_verify to False
    # If using http, set proto to http
    splunk_handler = SplunkHecHandler(host, token, 
                        port=port, proto='https', ssl_verify=False,
                        source=source)
    logger.addHandler(splunk_handler)
    
    return logger
    

