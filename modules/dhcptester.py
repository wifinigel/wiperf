'''
A simple class to perform a DHCP release & renew and return the renewal time
'''
from __future__ import print_function
import time
import subprocess
from modules.wirelessadapter import *


class DhcpTester(object):
    '''
    A class to perform a DHCP release & renew and return the renewal time
    '''

    def __init__(self, file_logger, debug=False, platform="rpi"):

        self.platform = platform
        self.debug = debug
        self.file_logger = file_logger

        self.interface = ''
        self.duration = ''
        self.debug = debug
        self.platform = platform

    def bounce_interface(self, interface, file_logger, debug):
        '''
        Log an error before bouncing the wlan interface
        '''
        import sys

        adapter = WirelessAdapter(interface, file_logger, self.platform, debug)
        self.file_logger.error("Bouncing WLAN interface")
        adapter.bounce_wlan_interface()
        self.file_logger.error("Interface bounced: {}".format(interface))

        # TODO: this exit will leave lock file in place - need to remove it
        # exit as something bad must have happened...
        sys.exit()

    def dhcp_renewal(self, interface, mode='passive'):
        '''
        This function will release the current DHCP address and request a renewal.
        The renewal duration is timed and the result (in mS) returned

        Usage:
            tester_obj = DhcpTester(logger, debug=False)
            tester_obj.dhcp_renewal("wlan0")

        If the renewal fails, the wlan interface will be bounced and the whole script will exit
        '''

        self.interface = interface

        if mode == 'active':

            # only do this if running active test
            if self.debug:
                print("Releasing dhcp address on {}...".format(self.interface))

            self.file_logger.info(
                "Releasing dhcp address on {}...".format(self.interface))
            try:
                # also includes zombie process tidy-up
                release_output = subprocess.check_output(
                    "sudo /sbin/dhclient -r -v {} -pf /tmp/dhclient.pid 2>&1 && sudo kill $(cat /tmp/dhclient.pid) 2> /dev/null".format(self.interface), shell=True).decode()
                # TODO: pattern search of: "DHCPRELEASE of 192.168.1.89 on wlan0"
                self.file_logger.info("Address released.")
                if self.debug:
                    print("Address released.")
            except Exception as ex:
                self.file_logger.error(
                    "Issue releasing IP on interface: {}, issue {}".format(self.interface, ex))
                if self.debug:
                    print("Issue releasing IP address: {}".format(ex))
                # If release fails, bounce interface to recover - script will exit
                self.bounce_interface(
                    self.interface, self.file_logger, self.debug)

        start = 0.0
        end = 0.0

        if self.debug:
            print("Renewing dhcp address...(mode = {})".format(mode))

        self.file_logger.info(
            "Renewing dhcp address...(mode = {}, interface= {})".format(mode, self.interface))
        try:
            # includes zombie process cleanup
            start = time.time()
            subprocess.check_output(
                "sudo /sbin/dhclient -v {} -1 -pf /tmp/dhclient.pid 2>&1 && sudo kill $(cat /tmp/dhclient.pid) 2> /dev/null".format(self.interface), shell=True).decode()
            end = time.time()
            # TODO: pattern search for "bound to 192.168.1.89"
            self.file_logger.info("Address renewed.")
            if self.debug:
                print("Address renewed.")
        except Exception as ex:
            self.file_logger.error("Issue renewing IP address: {}".format(ex))
            if self.debug:
                print("Issue renewing IP address: {}".format(ex))
            # If renewal fails, bounce interface to recover - script will exit
            self.bounce_interface(self.interface, self.file_logger, self.debug)

        self.duration = int(round((end - start) * 1000))

        self.file_logger.info("Renewal time: {}mS".format(self.duration))
        if self.debug:
            print("Renewal time: {}mS".format(self.duration))

        return self.duration

    def get_duration(self):
        ''' Get DHCP renewal duration '''
        return self.duration
