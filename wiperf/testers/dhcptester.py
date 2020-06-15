"""
A simple class to perform a DHCP release & renew and return the renewal time
"""
import time
import subprocess
from wiperf.helpers.wirelessadapter import WirelessAdapter


class DhcpTester(object):
    """
    A class to perform a DHCP release & renew and return the renewal time
    """

    def __init__(self, file_logger, platform="rpi"):

        self.platform = platform
        self.file_logger = file_logger

        self.interface = ''
        self.duration = ''
        self.platform = platform

    def bounce_interface(self, interface, file_logger):
        """
        Log an error before bouncing the wlan interface
        """
        import sys

        adapter = WirelessAdapter(interface, file_logger, self.platform)
        self.file_logger.error("Bouncing WLAN interface")
        adapter.bounce_wlan_interface()
        self.file_logger.error("Interface bounced: {}".format(interface))

        # TODO: this exit will leave lock file in place - need to remove it
        # exit as something bad must have happened...
        sys.exit()

    def dhcp_renewal(self, interface, mode='passive'):
        """
        This function will release the current DHCP address and request a renewal.
        The renewal duration is timed and the result (in mS) returned

        Usage:
            tester_obj = DhcpTester(logger, debug=False)
            tester_obj.dhcp_renewal("wlan0")

        If the renewal fails, the wlan interface will be bounced and the whole script will exit
        """

        self.interface = interface

        if mode == 'active':

            # only do this if running active test
            self.file_logger.debug("Releasing dhcp address on {}...".format(self.interface))

            self.file_logger.info(
                "Releasing dhcp address on {}...".format(self.interface))
            try:
                # also includes zombie process tidy-up
                release_output = subprocess.check_output(
                    "sudo /sbin/dhclient -r -v {} -pf /tmp/dhclient.pid 2>&1 && sudo kill $(cat /tmp/dhclient.pid) 2> /dev/null".format(self.interface), shell=True).decode()
                # TODO: pattern search of: "DHCPRELEASE of 192.168.1.89 on wlan0"
                self.file_logger.info("Address released.")
            except Exception as ex:
                self.file_logger.error("Issue releasing IP on interface: {}, issue {}".format(self.interface, ex))
                # If release fails, bounce interface to recover - script will exit
                self.bounce_interface(self.interface, self.file_logger)

        start = 0.0
        end = 0.0

        self.file_logger.info(
            "Renewing dhcp address...(mode = {}, interface= {})".format(mode, self.interface))
        try:
            # includes zombie process cleanup
            start = time.time()
            subprocess.check_output(
                "sudo /sbin/dhclient -v {} -pf /tmp/dhclient.pid 2>&1 && sudo kill $(cat /tmp/dhclient.pid) 2> /dev/null".format(self.interface), shell=True).decode()
            end = time.time()
            # TODO: pattern search for "bound to 192.168.1.89"
            self.file_logger.info("Address renewed.")
        except Exception as ex:
            self.file_logger.error("Issue renewing IP address: {}".format(ex))

            # If renewal fails, bounce interface to recover - script will exit
            self.bounce_interface(self.interface, self.file_logger)

        self.duration = int(round((end - start) * 1000))

        self.file_logger.info("Renewal time: {}mS".format(self.duration))

        return self.duration

    def run_tests(self, status_file_obj, config_vars, exporter_obj):

        self.file_logger.info("Starting DHCP renewal test...")
        status_file_obj.write_status_file("DHCP renew")

        # check mode to see which interface we need to use
        if config_vars['probe_mode'] == 'wireless':
            interface = config_vars['wlan_if']
        else:
            interface = config_vars['eth_if']

        self.file_logger.info("Interface under test: {}".format(interface))
        renewal_result = self.dhcp_renewal(interface, mode=config_vars['dhcp_test_mode'])

        if renewal_result:

            column_headers = ['time', 'renewal_time_ms']

            results_dict = {
                'time': int(time.time()),
                'renewal_time_ms': renewal_result,
            }

            # dump the results
            data_file = config_vars['dhcp_data_file']
            test_name = "DHCP"
            exporter_obj.send_results(config_vars, results_dict, column_headers, data_file, test_name, self.file_logger)

            self.file_logger.info("DHCP test ended.")

        else:
            self.file_logger.error("DHCP test error - no results (check logs)")

    def get_duration(self):
        """
        Get DHCP renewal duration
        """
        return self.duration
