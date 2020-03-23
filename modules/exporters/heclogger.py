'''
A function to perform logging to Splunk using the HTTP event logger (HEC).
'''
from splunk_http_event_collector import http_event_collector


def HecLogger(host, token, port, dict_data, source, file_logger):
    '''
    A function to perform logging to Splunk using the HTTP event logger (HEC).
    '''
    event_logger = http_event_collector(token, host)

    payload = {}
    payload.update({"sourcetype": "_json"})
    payload.update({"source": source})
    payload.update({"event": dict_data})
    event_logger.sendEvent(payload)
    event_logger.flushBatch()

    return True
