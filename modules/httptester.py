'''
A simple class to perform a http get and return the time taken
'''
import time
import socket
import requests
from requests.exceptions import HTTPError
from urllib.parse import urlparse


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
        self.http_get_result = 0

    def dns_lookup(self, http_target):
        '''
        This function will run a DNS lookup against the target supplied
        and return the results in a string.

        If the lookup fails, a False condition is returned with no further
        information (but info logged to system logger).

        Note that the http get is performed to the IP address after a silent
        DNS lookup to remove the DNS lookup delay to show the actual site
        response time.

        '''
        # pull out the hostname
        parse_obj = urlparse(http_target)
        hostname = parse_obj.hostname
        schema = parse_obj.scheme
        path = parse_obj.path
        port = parse_obj.port

        if not hostname:
            self.file_logger.error(
                "URL parsing failed for: {}".format(hostname))
            return False

        if self.debug:
            print("DNS test target: {}".format(hostname))

        if self.debug:
            print("Performing DNS lookup for: {}".format(hostname))

        try:
            target_ip = socket.gethostbyname(hostname)
        except Exception as ex:
            self.file_logger.error(
                "DNS test lookup to {} failed. Err msg: {}".format(hostname, ex))
            if self.debug:
                print("DNS lookup for: {} failed! - err: {}".format(hostname, ex))
                return False

        return [target_ip, schema, path, port]

    def http_get(self, http_target):
        '''
        This function will do a http/https get to the specifed target URL

        If the lookup fails, a False condition is returned with no further
        information. The lookup time is returned (results are in mS):

        '''

        if self.debug:
            print("HTTP test target: {}".format(http_target))

        '''
        # Get the IP address so that we don't included DNS lookup
        # time when performing http get

        dns_result = self.dns_lookup(http_target)
        target_ip = dns_result[0]
        schema = dns_result[1]
        path = dns_result[2]
        port = dns_result[3]

        if not port:
            port = '80'

        target_url = "{}://{}:{}{}".format(schema, target_ip, port, path)

        if not target_ip:
            self.file_logger.error(
                'DNS lookup error occurred to: {}'.format(http_target))
            return False

        if self.debug:
            print("Performing HTTP request to: {} ({})".format(
                target_ip, http_target))
        '''

        start = time.time()
        try:
            #response = requests.get(target_url, verify=False)
            response = requests.get(http_target, verify=False)

            # If the response was successful, no Exception will be raised
            response.raise_for_status()
        except HTTPError as http_err:
            self.file_logger.error('HTTP error occurred: {}'.format(http_err))
        except Exception as err:
            self.file_logger.error('Other error occurred: {}'.format(err))

        end = time.time()
        time_taken = int(round((end - start) * 1000))
        self.http_get_result = time_taken

        if self.debug:
            print("http get for: {} succeeded.".format(http_target))

        return self.http_get_result

    def get_http_get_result(self):
        ''' Get DNS lookup results '''
        return self.http_get_result
