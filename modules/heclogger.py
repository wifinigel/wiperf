'''
A class to perform logging to Splunk using the HTTP event logger (HEC).
'''
import logging
#from splunk_hec_handler import SplunkHecHandler
from splunk_http_event_collector import http_event_collector

def HecLogger(host, token, port, dict_data, source, file_logger, debug):
    '''
    A class to perform logging to Splunk using the HTTP event logger (HEC).
    '''

    #event_logger = http_event_collector(token, host, input_type='json', host='probe6', http_event_port=port, http_event_server_ssl=True)
    event_logger = http_event_collector(token, host)

    payload = {}
    #payload.update({"index":"test"})
    payload.update({"sourcetype":"_json"})
    payload.update({"source":source})
    #payload.update({"host":"wlanpi_probe6"})
    #payload.popNullFields = True
    payload.update({"event": dict_data})
    event_logger.sendEvent(payload)
    event_logger.flushBatch()
    
    #event_logger.sourcetype = '_json'
    #event_logger.index = 'history'
    #event_logger.debug = True

    return True
    '''

    logger = logging.getLogger('SplunkHecHandler')
    logger.setLevel(logging.INFO)

    file_logger.info("HecLogger: {}".format(source))

    # If using self-signed certificate, set ssl_verify to False
    # If using http, set proto to http
    splunk_handler = SplunkHecHandler(host, token, 
                        port=port, proto='https', ssl_verify=False,
                        source=source)
    logger.addHandler(splunk_handler)
    
    return logger
    '''

    

