import re
import subprocess
import sys
import time


class EthernetAdapter(object):

    '''
    A class to monitor and manipulate the wireless adapter for the WLANPerfAgent
    '''

    def __init__(self, eth_if_name, file_logger, platform="rpi"):

        self.eth_if_name = eth_if_name
        self.file_logger = file_logger
        self.platform = platform

        self.if_status = ''  # str
        self.ip_addr = ''  # str
        self.def_gw = ''  # str

        self.file_logger.debug("#### Initialized EthernetAdapter instance... ####")

    def field_extractor(self, field_name, pattern, cmd_output_text):

        re_result = re.search(pattern, cmd_output_text)

        if not re_result is None:
            field_value = re_result.group(1)

            self.file_logger.debug("{} = {}".format(field_name, field_value))

            return field_value
        else:

            return None

    def ifconfig(self):

        ####################################################################
        # Get wireless interface IP address info using the iwconfig command
        ####################################################################
        try:
            cmd = "/sbin/ip link show {}".format(self.eth_if_name)
            if_info = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True).decode()
        except subprocess.CalledProcessError as exc:
            output = exc.output.decode()
            error_descr = "Issue getting interface info using ip command: {}".format(output)

            self.file_logger.error("{}".format(error_descr))
            self.file_logger.error("Returning error...")
            return False

        self.file_logger.debug("Ethernet interface config info: {}".format(if_info))

        # Extract interface up/down status
        if not self.if_status:
            pattern = r'state (.*?) mode'
            field_name = "if_status"
            extraction = self.field_extractor(field_name, pattern, if_info)
            if extraction:
                self.if_status = extraction

        return True

    

    def get_ethernet_info(self):
        '''
        This function will look for various pieces of information from the
        wireless adapter which will be bundled with the speedtest results.

        It is a wrapper around the following commands, so will no doubt break at
        some stage:
            - iwconfig wlan0
            - iw dev wlan0 link
            - iw dev wlan0 info
            - iw dev wlan0 station dump

        The information provided may vary slightly between adapters and drivers, so is
        not guaranteed to be available in sall instances.

        We cannot assume all of the parameters below are available (sometimes
        they are missing for some reason until device is rebooted). Only
        provide info if they are available, otherwise replace with "NA"

        '''

        self.file_logger.debug("Getting wireless adapter info...")

        # get info using iwconfig cmd
        if self.ifconfig() == False:
            return False

        # get the values extracted and return in a list
        results_list = [self.if_status]

        self.file_logger.debug("Results list: {}".format(results_list))

        return results_list

    def get_adapter_ip(self):
        '''
        This method parses the output of the ifconfig command to figure out the
        IP address of the wireless adapter.

        As this is a wrapper around a CLI command, it is likely to break at
        some stage
        '''

        # Get interface info
        try:
            cmd = "/sbin/ip -4 a show  {}".format(self.eth_if_name)
            self.ifconfig_info = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True).decode()
        except subprocess.CalledProcessError as exc:
            output = exc.output.decode()
            error_descr = "Issue getting interface info using ip command to get IP info: {}".format(
                output)

            self.file_logger.error("{}".format(error_descr))
            self.file_logger.error("Returning error...")
            return False

        self.file_logger.debug("Interface config info: {}".format(self.ifconfig_info))

        # Extract IP address info (e.g. inet 10.255.250.157)
        ip_re = re.search(r'inet .*?(\d+\.\d+\.\d+\.\d+)', self.ifconfig_info)
        if ip_re is None:
            self.ip_addr = "NA"
        else:
            self.ip_addr = ip_re.group(1)

        # Check to see if IP address is APIPA (169.254.x.x)
        apipa_re = re.search(r'169\.254', self.ip_addr)
        if not apipa_re is None:
            self.ip_addr = "NA"

        self.file_logger.debug("IP Address = " + self.ip_addr)

        return self.ip_addr

    def get_route_info(self):
        '''
        This method parses the output of the route command to figure out the
        IP address of the ethernet adapter default gateway.

        As this is a wrapper around a CLI command, it is likely to break at
        some stage
        '''

        # Get route info (used to figure out default gateway)
        try:
            cmd = "/sbin/route -n | grep ^0.0.0.0 | grep {}".format(self.eth_if_name)
            self.route_info = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True).decode()
        except subprocess.CalledProcessError as exc:
            output = exc.output.decode()
            error_descr = "Issue getting default gateway info using route command (Prob due to multiple interfaces being up or wlan interface being wrong). Error: {}".format(
                str(output))

            self.file_logger.error(error_descr)
            self.file_logger.error("Returning error...")
            return False

        self.file_logger.debug("Route info: {}".format(self.route_info))

        # Extract def gw
        def_gw_re = re.search(
            r'0\.0\.0\.0\s+(\d+\.\d+\.\d+\.\d+)\s', self.route_info)
        if def_gw_re is None:
            self.def_gw = "NA"
        else:
            self.def_gw = def_gw_re.group(1)

        self.file_logger.debug("Default GW = " + self.def_gw)

    def bounce_eth_interface(self):
        '''
        If we run in to connectivity issues, we may like to try bouncing the
        wireless interface to see if we can recover the connection.

        Note: wlanpi must be added to sudoers group using visudo command on RPI
        '''

        self.file_logger.debug("Bouncing interface (platform type = " + self.platform + ")")

        self.file_logger.info("Bouncing interface {} (platform type = {})".format(self.eth_if_name, self.platform))

        if_bounce_cmd = "sudo /sbin/ifdown {} && sudo /sbin/ifup {};".format(self.eth_if_name, self.eth_if_name)

        self.file_logger.debug("if bounce command: {}".format(if_bounce_cmd))

        try:
            if_bounce = subprocess.check_output(if_bounce_cmd, stderr=subprocess.STDOUT, shell=True).decode()
        except subprocess.CalledProcessError as exc:
            output = exc.output.decode()
            error_descr = "i/f bounce command appears to have failed. Error: {}".format(str(output))

            self.file_logger.error(error_descr)
            self.file_logger.error("Returning error...")
            return False

        return True
    
    def bounce_error_exit(self, lockf_obj):
        '''
        Log an error before bouncing the eth interface and then exiting as we have an unrecoverable error with the network connection
        '''
        import sys

        self.file_logger.error("Attempting to recover by bouncing ethernet interface...")
        self.file_logger.error("Bouncing Ethernet interface")
        self.bounce_eth_interface()
        self.file_logger.error("Bounce completed. Exiting script.")

        # clean up lock file & exit
        lockf_obj.delete_lock_file()
        sys.exit()

    def get_if_status(self):
        return self.if_status

    def get_ipaddr(self):
        return self.ip_addr

    def get_def_gw(self):
        return self.def_gw
