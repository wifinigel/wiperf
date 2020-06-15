import sys
import time
import subprocess
from socket import gethostbyname

from wiperf.helpers.ethernetadapter import EthernetAdapter
from wiperf.testers.mgtconnectiontester import MgtConnectionTester

class EthernetConnectionTester(object):
    """
    Class to implement ethernet network connection tests for wiperf
    """

    def __init__(self, file_logger, interface, platform):

        self.platform = platform
        self.file_logger = file_logger
        self.adapter_obj = EthernetAdapter(interface, self.file_logger, platform)

    def run_tests(self, watchdog_obj, lockf_obj, config_vars, exporter_obj):

        # if we have no network connection (i.e. link down or no IP), no point in proceeding...
        self.file_logger.info("Checking ethernet connection available.")
        if self.adapter_obj.get_ethernet_info() == False:

            self.file_logger.error("Unable to get ethernet info due to failure with ifconfig command")
            watchdog_obj.inc_watchdog_count()
            self.adapter_obj.bounce_error_exit(lockf_obj)  # exit here

        self.file_logger.info("Checking we have an IP address.")
        # if we have no IP address, no point in proceeding...
        if self.adapter_obj.get_adapter_ip() == False:
            self.file_logger.error("Unable to get ethernet adapter IP info")
            watchdog_obj.inc_watchdog_count()
            self.adapter_obj.bounce_error_exit(lockf_obj)  # exit here

        # TODO: Fix this. Currently breaks when we have Eth & Wireless ports both up
        '''
        if self.adapter_obj.get_route_info() == False:
            file_logger.error("Unable to get wireless adapter route info - maybe you have multiple interfaces enabled that are stopping the wlan interface being used?")
            self.adapter_obj.bounce_error_exit(lockf_obj) # exit here
        '''

        if self.adapter_obj.get_ipaddr() == 'NA':
            self.file_logger.error("Problem with ethernet connection: no valid IP address")
            watchdog_obj.inc_watchdog_count()
            self.adapter_obj.bounce_error_exit(lockf_obj) # exit here

        # final connectivity check: see if we can resolve an address
        # (network connection and DNS must be up)
        self.file_logger.info("Checking we can do a DNS lookup to {}".format(config_vars['connectivity_lookup']))
        try:
            gethostbyname(config_vars['connectivity_lookup'])
        except Exception as ex:
            self.file_logger.error(
                "DNS seems to be failing, bouncing ethernet interface. Err msg: {}".format(ex))
            watchdog_obj.inc_watchdog_count()
            self.adapter_obj.bounce_error_exit(lockf_obj)  # exit here

        # Check we can get to the mgt platform (function will exit script if no connectivity)
        self.file_logger.info("Checking we can get to the management platform...")

        mgt_connection_obj = MgtConnectionTester(config_vars, self.file_logger, self.platform)
        mgt_connection_obj.check_connection(watchdog_obj, lockf_obj)
