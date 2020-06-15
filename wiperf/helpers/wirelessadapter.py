import re
import subprocess
import sys
import time


class WirelessAdapter(object):

    '''
    A class to monitor and manipulate the wireless adapter for the WLANPerfAgent
    '''

    def __init__(self, wlan_if_name, file_logger, platform="rpi"):

        self.wlan_if_name = wlan_if_name
        self.file_logger = file_logger
        self.platform = platform

        self.ssid = ''  # str
        self.bssid = ''  # str
        self.freq = False  # float
        self.center_freq = False  # float
        self.channel = False  # int
        self.channel_width = False  # int
        self.tx_bit_rate = False  # float
        self.rx_bit_rate = False  # float
        self.tx_mcs = False  # int
        self.rx_mcs = False  # int

        self.signal_level = False  # float
        self.tx_retries = False  # int

        self.ip_addr = ''  # str
        self.def_gw = ''  # str

        self.file_logger.debug("#### Initialized WirelessAdapter instance... ####")

    def field_extractor(self, field_name, pattern, cmd_output_text):

        re_result = re.search(pattern, cmd_output_text)

        if not re_result is None:
            field_value = re_result.group(1)

            self.file_logger.debug("{} = {}".format(field_name, field_value))

            return field_value
        else:

            return None

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
            cmd = "/sbin/iwconfig {}".format(self.wlan_if_name)
            iwconfig_info = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True).decode()
        except subprocess.CalledProcessError as exc:
            output = exc.output.decode()
            error_descr = "Issue getting interface info using iwconfig command: {}".format(output)

            self.file_logger.error("{}".format(error_descr))
            self.file_logger.error("Returning error...")
            return False

        self.file_logger.debug("Wireless interface config info: {}".format(iwconfig_info))

        # Extract SSID
        if not self.ssid:
            pattern = r'ESSID\:\"(.*?)\"'
            field_name = "ssid"
            extraction = self.field_extractor(
                field_name, pattern, iwconfig_info)
            if extraction:
                self.ssid = extraction

        # Extract BSSID (Note that if WLAN adapter not associated, "Access Point: Not-Associated")
        if not self.bssid:
            pattern = r'Access Point[\=|\:] (..\:..\:..\:..\:..\:..)'
            field_name = "bssid"
            extraction = self.field_extractor(
                field_name, pattern, iwconfig_info)
            if extraction:
                self.bssid = extraction

        # Extract Frequency
        if not self.freq:
            pattern = r'Frequency[\:|\=](\d+\.\d+) '
            field_name = "freq"
            extraction = self.field_extractor(
                field_name, pattern, iwconfig_info)
            if extraction:
                self.freq = float(extraction)

        # lookup channel number from freq
        self.channel = self.channel_lookup(str(self.freq))

        # Extract Tx Bit Rate (e.g. Bit Rate=144.4 Mb/s)
        if not self.tx_bit_rate:
            pattern = r'Bit Rate[\=|\:]([\d|\.]+) '
            field_name = "tx_bit_rate"
            extraction = self.field_extractor(
                field_name, pattern, iwconfig_info)
            if extraction:
                self.tx_bit_rate = float(extraction)

        # Extract Signal Level
        if not self.signal_level:
            pattern = r'Signal level[\=|\:](.+?) dBm'
            field_name = "signal_level"
            extraction = self.field_extractor(
                field_name, pattern, iwconfig_info)
            if extraction:
                self.signal_level = float(extraction)

        # Extract tx retries
        if not self.tx_retries:
            pattern = r'Tx excessive retries[\=|\:](\d+?) '
            field_name = "tx_retries"
            extraction = self.field_extractor(
                field_name, pattern, iwconfig_info)
            if extraction:
                self.tx_retries = int(extraction)

        return True

    def iw_info(self):

         #############################################################################
        # Get wireless interface IP address info using the iw dev wlanX info command
        #############################################################################
        try:
            cmd = "/sbin/iw {} info".format(self.wlan_if_name)
            iw_info = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True).decode()
        except subprocess.CalledProcessError as exc:
            output = exc.output.decode()
            error_descr = "Issue getting interface info using iw info command: {}".format(
                output)

            self.file_logger.error("{}".format(error_descr))
            self.file_logger.error("Returning error...")
            return False

        self.file_logger.debug("Wireless interface config info (iw dev wlanX info): {}".format(iw_info))

        # Extract channel width
        if not self.channel_width:
            pattern = r'width\: (\d+) MHz'
            field_name = "channel_width"
            extraction = self.field_extractor(
                field_name, pattern, iw_info)
            if extraction:
                self.channel_width = int(extraction)

        # Extract center freq
        if not self.center_freq:
            pattern = r'center1\: (\d+) MHz'
            field_name = "center_freq"
            extraction = self.field_extractor(
                field_name, pattern, iw_info)
            if extraction:
                self.center_freq = float(extraction)/1000

        # Extract frequency
        if not self.freq:
            pattern = r'channel \d+ \((\d+) MHz\)'
            field_name = "freq"
            extraction = self.field_extractor(
                field_name, pattern, iw_info)
            if extraction:
                self.freq = float(extraction)/1000

        return True

    def iw_link(self):

         #############################################################################
        # Get wireless interface IP address info using the iw dev wlanX link command
        #############################################################################
        try:
            cmd = "/sbin/iw {} link".format(self.wlan_if_name)
            iw_link = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True).decode()
        except subprocess.CalledProcessError as exc:
            output = exc.output.decode()
            error_descr = "Issue getting interface info using iw link command: {}".format(output)

            self.file_logger.error("{}".format(error_descr))
            self.file_logger.error("Returning error...")
            return False

        self.file_logger.debug("Wireless interface config info (iw dev wlanX link): {}".format(iw_link))

        # Extract channel width
        if not self.channel_width:
            pattern = r' (\d+)MHZ '
            field_name = "channel_width"
            extraction = self.field_extractor(
                field_name, pattern, iw_link)
            if extraction:
                self.channel_width = int(extraction)

        # Extract Signal Level
        if not self.signal_level:
            pattern = r'signal: (\-\d+) dBm'
            field_name = "signal_level"
            extraction = self.field_extractor(
                field_name, pattern, iw_link)
            if extraction:
                self.signal_level = float(extraction)

        # Extract Tx Bit Rate (e.g. tx bitrate: 150.0 MBit/s)
        if not self.tx_bit_rate:
            pattern = r'tx bitrate: ([\d|\.]+) MBit/s'
            field_name = "tx_bit_rate"
            extraction = self.field_extractor(
                field_name, pattern, iw_link)
            if extraction:
                self.tx_bit_rate = float(extraction)

        # Extract MCS value (e.g. tx bitrate: 150.0 MBit/s MCS 7 40MHz short GI)
        if not self.tx_mcs:
            pattern = r' MCS (\d+) '
            field_name = "tx_mcs"
            extraction = self.field_extractor(
                field_name, pattern, iw_link)
            if extraction:
                self.tx_mcs = int(extraction)

        return True

    def iw_station(self):

         #####################################################################################
        # Get wireless interface IP address info using the iw dev wlanX station dump command
        ######################################################################################
        try:
            cmd = "/sbin/iw {} station dump".format(self.wlan_if_name)
            iw_station = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True).decode()
        except subprocess.CalledProcessError as exc:
            output = exc.output.decode()
            error_descr = "Issue getting interface info using iw station command: {}".format(output)

            self.file_logger.error("{}".format(error_descr))
            self.file_logger.error("Returning error...")
            return False

        self.file_logger.debug("Wireless interface config info (iw dev wlanX station dump): {}".format(iw_station))

        # Extract channel width
        if not self.channel_width:
            pattern = r'rx bitrate\:.*?(\d+)MHz'
            field_name = "channel_width"
            extraction = self.field_extractor(field_name, pattern, iw_station)
            if extraction:
                self.channel_width = int(extraction)

        # Extract Tx Bit Rate (e.g. tx bitrate:     72.2 MBit/s MCS 7 short GI)
        if not self.tx_bit_rate:
            pattern = r'tx bitrate\:.*?([\d|\.]+) MBit/s'
            field_name = "tx_bit_rate"
            extraction = self.field_extractor(field_name, pattern, iw_station)
            if extraction:
                self.tx_bit_rate = float(extraction)

        # Extract Rx Bit Rate (e.g. rx bitrate:     121.5 MBit/s MCS 6 40MHz)
        if not self.rx_bit_rate:
            pattern = r'rx bitrate\:.*?([\d|\.]+) MBit/s'
            field_name = "rx_bit_rate"
            extraction = self.field_extractor(field_name, pattern, iw_station)
            if extraction:
                self.rx_bit_rate = float(extraction)

        # Extract Tx MCS value (e.g. tx bitrate:     72.2 MBit/s MCS 7 short GI)
        if not self.tx_mcs:
            pattern = r'tx bitrate\:.*?MCS (\d+) '
            field_name = "tx_mcs"
            extraction = self.field_extractor(field_name, pattern, iw_station)
            if extraction:
                self.tx_mcs = int(extraction)

        # Extract Rx MCS value (e.g. rx bitrate:     121.5 MBit/s MCS 6 40MHz)
        if not self.rx_mcs:
            pattern = r'rx bitrate\:.*?MCS (\d+)'
            field_name = "rx_mcs"
            extraction = self.field_extractor(field_name, pattern, iw_station)
            if extraction:
                self.rx_mcs = int(extraction)

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

        self.file_logger.debug("Getting wireless adapter info...")

        # get info using iwconfig cmd
        if self.iwconfig() == False:
            return False

        # get info using iw info
        if self.iw_info() == False:
            return False

        # get info using iw link
        if self.iw_link() == False:
            return False

        # get info using iw station
        if self.iw_station() == False:
            return False

        # get the values extracted and return in a list
        results_list = [self.ssid, self.bssid, self.freq, self.tx_bit_rate,
                        self.signal_level, self.tx_retries, self.channel]

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
            cmd = "/sbin/ifconfig {}".format(self.wlan_if_name)
            self.ifconfig_info = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True).decode()
        except subprocess.CalledProcessError as exc:
            output = exc.output.decode()
            error_descr = "Issue getting interface info using iw station command: {}".format(
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
        IP address of the wireless adapter default gateway.

        As this is a wrapper around a CLI command, it is likely to break at
        some stage
        '''

        # Get route info (used to figure out default gateway)
        try:
            cmd = "/sbin/route -n | grep ^0.0.0.0 | grep {}".format(self.wlan_if_name)
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

    def bounce_wlan_interface(self):
        '''
        If we run in to connectivity issues, we may like to try bouncing the
        wireless interface to see if we can recover the connection.

        Note: wlanpi must be added to sudoers group using visudo command on RPI
        '''

        self.file_logger.debug("Bouncing interface (platform type = " + self.platform + ")")

        self.file_logger.info(
            "Bouncing interface {} (platform type = {})".format(self.wlan_if_name, self.platform))

        if_bounce_cmd = "sudo /sbin/ifdown {} && sudo /sbin/ifup {};".format(self.wlan_if_name, self.wlan_if_name)

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
        Log an error before bouncing the wlan interface and then exiting as we have an unrecoverable error with the network connection
        '''
        import sys

        self.file_logger.error("Attempting to recover by bouncing wireless interface...")
        self.file_logger.error("Bouncing WLAN interface")
        self.bounce_wlan_interface()
        self.file_logger.error("Bounce completed. Exiting script.")

        # clean up lock file & exit
        lockf_obj.delete_lock_file()
        sys.exit()

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
