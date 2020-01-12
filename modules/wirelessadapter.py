import re
import subprocess
import sys
import time


class WirelessAdapter(object):

    '''
    A class to monitor and manipulate the wireless adapter for the WLANPerfAgent
    '''

    def __init__(self, wlan_if_name, file_logger, platform="rpi", debug=False):

        self.wlan_if_name = wlan_if_name
        self.file_logger = file_logger
        self.platform = platform
        self.debug = debug

        self.ssid = ''
        self.bssid = ''
        self.freq = ''
        self.center_freq = ''
        self.channel = ''
        self.channel_width = ''
        self.tx_bit_rate = 0
        self.rx_bit_rate = 0
        self.tx_mcs = 0
        self.rx_mcs = 0

        self.signal_level = 0
        self.tx_retries = 0

        self.ip_addr = ''
        self.def_gw = ''

        if self.debug:
            print("#### Initialized WirelessAdapter instance... ####")

    def field_extractor(self, field_name, pattern, cmd_output_text):

        field_value = "NA"

        re_result = re.search(pattern, cmd_output_text)

        if not re_result is None:
            field_value = re_result.group(1)

        if self.debug:
            print("{} = {}".format(field_name, field_value))

        return field_value

    def channel_lookup(self, freq):

        channels = {
            '2.412': 1,
            '2.417': 2,
            '2.422': 3,
            '2.427': 4,
            '2.432': 5,
            '2.437': 6,
            '2.442': 7,
            '2.447': 8,
            '2.452': 9,
            '2.457': 10,
            '2.462': 11,
            '2.467': 12,
            '2.472': 13,
            '2.484': 14,
            '5.18':  36,
            '5.2':  40,
            '5.22':  44,
            '5.24':  48,
            '5.26':  52,
            '5.28':  56,
            '5.3':   60,
            '5.32':  64,
            '5.5':   100,
            '5.52':  104,
            '5.54':  108,
            '5.56':  112,
            '5.58':  116,
            '5.6':   120,
            '5.62':  124,
            '5.64':  128,
            '5.66':  132,
            '5.68':  136,
            '5.7':   140,
            '5.72':  144,
            '5.745': 149,
            '5.765': 153,
            '5.785': 157,
            '5.805': 161,
            '5.825': 165,
        }

        return channels.get(freq, 'unknown')

    def iwconfig(self):

        ####################################################################
        # Get wireless interface IP address info using the iwconfig command
        ####################################################################
        try:
            iwconfig_info = subprocess.check_output(
                "/sbin/iwconfig " + self.wlan_if_name + " 2>&1", shell=True).decode()
        except Exception as ex:
            error_descr = "Issue getting interface info using iwconfig command"
            if self.debug:
                print("{}: {}".format(error_descr, ex))

            self.file_logger.error("{}: {}".format(error_descr, ex))
            self.file_logger.error("Returning error...")
            return False

        if self.debug:
            print("Wireless interface config info: ")
            print(iwconfig_info)

        # Extract SSID
        if not self.ssid:
            pattern = 'ESSID\:\"(.*?)\"'
            field_name = "ssid"
            self.ssid = self.field_extractor(
                field_name, pattern, iwconfig_info)

        # Extract BSSID (Note that if WLAN adapter not associated, "Access Point: Not-Associated")
        if not self.bssid:
            pattern = 'Access Point[\=|\:] (..\:..\:..\:..\:..\:..)'
            field_name = "bssid"
            self.bssid = self.field_extractor(
                field_name, pattern, iwconfig_info)

        # Extract Frequency
        if not self.freq:
            pattern = 'Frequency[\:|\=](\d+\.\d+) '
            field_name = "freq"
            self.freq = self.field_extractor(
                field_name, pattern, iwconfig_info)

        # lookup channel number
        self.channel = self.channel_lookup(self.freq)

        # Extract Bit Rate (e.g. Bit Rate=144.4 Mb/s)
        ssid_re = re.search('Bit Rate[\=|\:]([\d|\.]+) ', iwconfig_info)
        if ssid_re is None:
            self.tx_bit_rate = "NA"
        else:
            self.tx_bit_rate = ssid_re.group(1)

        if self.debug:
            print("Bit rate: " + self.tx_bit_rate)

        # Extract Signal Level
        ssid_re = re.search('Signal level[\=|\:](.+?) ', iwconfig_info)
        if ssid_re is None:
            self.signal_level = "NA"
        else:
            self.signal_level = ssid_re.group(1)

        if self.debug:
            print("Signal level = " + self.signal_level)

        # Extract tx retries
        ssid_re = re.search(
            'Tx excessive retries[\=|\:](\d+?) ', iwconfig_info)
        if ssid_re is None:
            self.tx_retries = "NA"
        else:
            self.tx_retries = ssid_re.group(1)

        if self.debug:
            print("Excessive Tx Retries = " + self.tx_retries)

        return True

    def iw_info(self):

         #############################################################################
        # Get wireless interface IP address info using the iw dev wlanX info command
        #############################################################################
        try:
            iw_info = subprocess.check_output(
                "/sbin/iw " + self.wlan_if_name + " info 2>&1", shell=True).decode()
        except Exception as ex:
            error_descr = "Issue getting interface info using iwconfig command"
            if self.debug:
                print("{}: {}".format(error_descr, ex))

            self.file_logger.error("{}: {}".format(error_descr, ex))
            self.file_logger.error("Returning error...")
            return False

        if self.debug:
            print("Wireless interface config info (iw dev wlanX info): ")
            print(iw_info)

        # Extract channel width
        if not self.channel_width:
            pattern = 'width\: (\d+) MHz'
            field_name = "channel_width"
            self.channel_width = self.field_extractor(
                field_name, pattern, iw_info)

        # Extract center freq
        if not self.center_freq:
            pattern = 'center1\: (\d+) MHz'
            field_name = "center_freq"
            self.center_freq = self.field_extractor(
                field_name, pattern, iw_info)

        # Extract frequency
        if not self.freq:
            pattern = 'channel \d+ \((\d+) MHz\)'
            field_name = "freq"
            self.freq = self.field_extractor(
                field_name, pattern, iw_info)

        return True

    def get_wireless_info(self):
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

        if self.debug:
            print("Getting wireless adapter info...")

        # get info using iwconfig cmd
        self.iwconfig()

        # get info using iw info
        self.iw_info()

        # get info using iw link
        # self.iw_link(self)

        # get info using iw station
        # self.iw_link(self)

        # get the values extracted and return in a list
        results_list = [self.ssid, self.bssid, self.freq, self.tx_bit_rate,
                        self.signal_level, self.tx_retries, self.channel]

        if self.debug:
            print("Results list:")
            print(results_list)

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
            self.ifconfig_info = subprocess.check_output(
                "/sbin/ifconfig " + str(self.wlan_if_name) + " 2>&1", shell=True).decode()
        except Exception as ex:
            error_descr = "Issue getting interface info using ifconfig command"
            if self.debug:
                print(error_descr)
                print(ex)

            self.file_logger.error(error_descr)
            self.file_logger.error(ex)
            self.file_logger.error("Return error...")
            return False

        if self.debug:
            print("Interface config info: ")
            print(self.ifconfig_info)

        # Extract IP address info (e.g. inet 10.255.250.157)
        ip_re = re.search('inet .*?(\d+\.\d+\.\d+\.\d+)', self.ifconfig_info)
        if ip_re is None:
            self.ip_addr = "NA"
        else:
            self.ip_addr = ip_re.group(1)

        # Check to see if IP address is APIPA (169.254.x.x)
        apipa_re = re.search('169\.254', self.ip_addr)
        if not apipa_re is None:
            self.ip_addr = "NA"

        if self.debug:
            print("IP Address = " + self.ip_addr)

        return self.ip_addr

    def get_route_info(self):
        '''
        This method parses the output of the route command to figure out the
        IP address of the wireless adapter default gateway.

        As this is a wrapper around a CLI command, it is likely to break at
        some stage
        '''

        # Get route info (used to figure out default gateway)
        try:
            self.route_info = subprocess.check_output(
                "/sbin/route -n | grep ^0.0.0.0 | grep " + self.wlan_if_name + " 2>&1", shell=True).decode()
        except Exception as ex:
            error_descr = "Issue getting default gateway info using route command (Prob due to multiple interfaces being up or wlan interface being wrong)"
            if self.debug:
                print(error_descr)
                print(ex)

            self.file_logger.error(error_descr)
            self.file_logger.error(ex)
            self.file_logger.error("Returning error...")
            return False

        if self.debug:
            print("Route info:")
            print(self.route_info)

        # Extract def gw
        def_gw_re = re.search(
            '0\.0\.0\.0\s+(\d+\.\d+\.\d+\.\d+)\s', self.route_info)
        if def_gw_re is None:
            self.def_gw = "NA"
        else:
            self.def_gw = def_gw_re.group(1)

        if self.debug:
            print("Default GW = " + self.def_gw)

    def bounce_wlan_interface(self):
        '''
        If we run in to connectivity issues, we may like to try bouncing the
        wireless interface to see if we can recover the connection.

        Note: wlanpi must be added to sudoers group using visudo command on RPI
        '''

        if self.debug:
            print("Bouncing interface (platform type = " + self.platform + ")")

        self.file_logger.error(
            "Bouncing interface (platform type = " + self.platform + ")")

        if_down_cmd = "sudo /sbin/ifconfig {} down".format(self.wlan_if_name)

        if self.debug:
            print("if down command:")
            print(if_down_cmd)

        try:
            if_down = subprocess.check_output(
                if_down_cmd, stderr=subprocess.STDOUT, shell=True).decode()
        except Exception as ex:
            error_descr = "ifdown command appears to have failed"
            if self.debug:
                print(error_descr)
                print(ex)

            self.file_logger.error(error_descr)
            self.file_logger.error(ex)
            self.file_logger.error("Returning error...")
            return False

        if self.debug:
            print("")
            print("Output of ifdown command: ")
            print(if_down)

        self.file_logger.error("sudo ifdown output: " + str(if_down))

        # have a sleep to allow time for wpa_supplicant to exit?
        time.sleep(5)

        # if_up_cmd = "sudo ifup " + str(self.wlan_if_name)
        if_up_cmd = "sudo /sbin/ifconfig {} up".format(self.wlan_if_name)

        if self.debug:
            print("if up command:")
            print(if_up_cmd)

        try:
            if_up = subprocess.check_output(
                if_up_cmd, stderr=subprocess.STDOUT, shell=True).decode()
        except Exception as ex:
            error_descr = "ifup command appears to have failed"
            if self.debug:
                print(error_descr)
                print(ex)

            self.file_logger.error(error_descr)
            self.file_logger.error(ex)
            self.file_logger.error("Returning error...")
            return False

        if self.debug:
            print("Output of ifup command: ")
            print(if_up)

        self.file_logger.error("sudo ifup output: " + str(if_up))

        return True

    def get_ssid(self):
        return self.ssid

    def get_bssid(self):
        return self.bssid

    def get_freq(self):
        return self.freq

    def get_center_freq(self):
        return self.center_freq

    def get_channel(self):
        return self.channel

    def get_channel_width(self):
        return self.channel_width

    def get_tx_bit_rate(self):
        return self.tx_bit_rate

    def get_rx_bit_rate(self):
        return self.rx_bit_rate

    def get_tx_mcs(self):
        return self.tx_mcs

    def get_rx_mcs(self):
        return self.rx_mcs

    def get_signal_level(self):
        return self.signal_level

    def get_tx_retries(self):
        return self.tx_retries

    def get_ipaddr(self):
        return self.ip_addr

    def get_def_gw(self):
        return self.def_gw
