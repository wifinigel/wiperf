'''
A simple class to perform a DNS lookup against a number of targets and return the lookup time
'''
from __future__ import print_function
import time
import socket


class DnsTester(object):
    '''
    A class to perform a number of DNS lookups and return the lookup times
    '''

    def __init__(self, file_logger, debug=False, platform="rpi"):

        self.platform = platform
        self.debug = debug
        self.file_logger = file_logger

        self.targets = []
        self.dns_results = {}

    def dns_lookup(self, targets):
        '''
        This function will run a series of DNS lookups against the targets supplied
        and return the results in a dictionary.

        Usage:
            tester_obj.dns_lookup(['google.com', 'cisco.com', 'bbc.co.uk'])
        
        If the lookup fails, a False condition is returned with no further
        information. The following dictionary is returned (results are in mS):

        {   'google.com': 45,
            'cisco.com': 52,
            'bbc.co.uk': 33,
        }
        '''
        # TODO: How do we handle empty targets & lookup failures (e.g. bad name)

        self.targets = targets

        if self.debug:
                print("DNS test targets: {}".format(self.targets))

        for target in self.targets:

            if self.debug:
                print("Performing DNS lookup for: {}".format(target))

            start = time.time()
            try:
                socket.gethostbyname(target)
            except Exception as ex:
                self.file_logger.error("DNS test lookup to {} failed. Err msg: {}".format(target, ex))
                self.dns_results[target] = ''
                if self.debug:
                    print("DNS lookup for: {} failed! - err: {}".format(target, ex))
                continue

            end = time.time()
            time_taken = int(round((end - start) * 1000))
            self.dns_results[target] = time_taken

            if self.debug:
                    print("DNS lookup for: {} succeeded.".format(target))

        return self.dns_results


    def get_dns_results(self):
        ''' Get DNS lookup results '''
        return self.dns_results

