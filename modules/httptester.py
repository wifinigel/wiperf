'''
A simple class to perform a http get and return the time taken
'''
import time
import socket
import requests
from requests.exceptions import HTTPError


class HttpTester(object):
    '''
    A simple class to perform a http get and return the time taken
    '''

    def __init__(self, file_logger, debug=False, platform="rpi"):

        self.platform = platform
        self.debug = debug
        self.file_logger = file_logger

        self.http_target = ''
        self.target_ip = ''
        self.http_get_duration = 0
        self.http_status_code = 0

    def http_get(self, http_target):
        '''
        This function will do a http/https get to the specifed target URL

        If the lookup fails, a False condition is returned with no further
        information. The lookup time is returned (results are in mS):

        '''

        if self.debug:
            print("HTTP test target: {}".format(http_target))

        start = time.time()
        try:
            #response = requests.get(target_url, verify=False)
            response = requests.get(http_target, verify=False)
            self.http_status_code = response.status_code

            # If the response was successful, no Exception will be raised
            response.raise_for_status()
        except HTTPError as http_err:
            self.file_logger.error('HTTP error occurred: {}'.format(http_err))
        except Exception as err:
            self.file_logger.error('Other error occurred: {}'.format(err))

        end = time.time()
        time_taken = int(round((end - start) * 1000))
        self.http_get_duration = time_taken

        if self.debug:
            print("http get for: {} succeeded.".format(http_target))

        # return status code & elapsed duration in mS
        return (self.http_status_code, self.http_get_duration)

    def get_http_duration(self):
        ''' Get DNS lookup results '''
        return self.http_get_duration

    def get_status_code(self):
        ''' Get http status code '''
        return self.http_status_code
