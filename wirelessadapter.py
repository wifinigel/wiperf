
class WirelessAdapter(object):

    '''
    A class to monitor and manipulate the wireless adapter for the WLANPerfAgent
    '''

    def __init__(self, wlan_if_name, file_logger, platform="rpi", debug=False):
    
        import sys
        
        self.wlan_if_name = wlan_if_name
        self.file_logger = file_logger
        self.platform = platform
        self.debug = debug
        
        self.ssid = ''
        self.bssid = ''
        self.freq = ''
        self.bit_rate = ''
        self.signal_level = ''
        
        self.ip_addr = ''
        self.def_gw = ''

        if self.debug:
            print("#### Initialized WirelessAdapter instance... ####")
        
    def get_wireless_info(self):

        '''
        This function will look for various pieces of information from the 
        wireless adapter which will be bundled with the speedtest results.
        
        It is a wrapper around the "iwconfig wlanx", so will no doubt break at
        some stage. 
        
        We cannot assume all of the parameters below are available (sometimes
        they are missing for some reason until device is rebooted). Only
        provide info if they are available, otherwise replace with "NA"

        '''
        import re
        import subprocess

        if self.debug:
            print("Getting wireless adapter info...")
        
        # Get wireless interface IP address info
        try:
            self.iwconfig_info = subprocess.check_output("/sbin/iwconfig " + self.wlan_if_name + " 2>&1", shell=True)
        except Exception as ex:
            error_descr = "Issue getting interface info using iwconfig command"
            if self.debug:
                print(error_descr)
                print(ex)
            
            self.file_logger.error(error_descr)
            self.file_logger.error(ex)
            self.file_logger.error("Returning error...")
            return False
            
        if self.debug:
            print("Wireless interface config info: ")
            print(self.iwconfig_info)
        
        # Extract SSID
        ssid_re = re.search('ESSID\:\"(.*?)\"', self.iwconfig_info)
        if ssid_re is None:
            self.ssid = "NA"
        else:            
            self.ssid = ssid_re.group(1)
        
        if self.debug:
            print("SSID = " + self.ssid)
        
        # Extract BSSID (Note that if WLAN adapter not associated, "Access Point: Not-Associated")
        ssid_re = re.search('Access Point[\=|\:] (..\:..\:..\:..\:..\:..)', self.iwconfig_info)
        if ssid_re is None:
            self.bssid = "NA"
        else:            
            self.bssid = ssid_re.group(1)
        
        if self.debug:
            print("BSSID = " + self.bssid)
        
        # Extract Frequency
        ssid_re = re.search('Frequency[\:|\=](\d+\.\d+) ', self.iwconfig_info)
        if ssid_re is None:
            self.freq = "NA"
        else:        
            self.freq = ssid_re.group(1)
        
        if self.debug:
            print("Frequency = " + self.freq)
        
        # Extract Bit Rate (e.g. Bit Rate=144.4 Mb/s)
        ssid_re = re.search('Bit Rate[\=|\:]([\d|\.]+) ', self.iwconfig_info)
        if ssid_re is None:
            self.bit_rate = "NA"
        else:        
            self.bit_rate = ssid_re.group(1)
        
        if self.debug:
            print("Bit rate: " + self.bit_rate)
        
        
        # Extract Signal Level
        ssid_re = re.search('Signal level[\=|\:](.+?) ', self.iwconfig_info)
        if ssid_re is None:
            self.signal_level = "NA"
        else:
            self.signal_level = ssid_re.group(1)
            
        if self.debug:
            print("Signal level = " + self.signal_level)
        
        results_list = [self.ssid, self.bssid, self.freq, self.bit_rate, self.signal_level]

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
        
        import re
        import subprocess
        
        # Get interface info
        try:            
            self.ifconfig_info = subprocess.check_output("/sbin/ifconfig " + str(self.wlan_if_name) + " 2>&1", shell=True)
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
    
        import re
        import subprocess
        
        # Get route info (used to figure out default gateway)
        try:
            self.route_info = subprocess.check_output("/sbin/route -n | grep ^0.0.0.0 | grep " + self.wlan_if_name + " 2>&1", shell=True)
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
        def_gw_re = re.search('0\.0\.0\.0\s+(\d+\.\d+\.\d+\.\d+)\s', self.route_info)
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
        import subprocess
        
        if self.debug:
            print("Bouncing interface (platform type = " + self.platform + ")")
        
        self.file_logger.error("Bouncing interface (platform type = " + self.platform + ")")
        
        if_down_cmd = "sudo ifdown " + str(self.wlan_if_name)
        
        
        if self.debug:
            print("if down command:")
            print(if_down_cmd)

        try:        
            if_down = subprocess.check_output(if_down_cmd, stderr=subprocess.STDOUT, shell=True)
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
            print (if_down)
            
        self.file_logger.error("sudo ifdown output: " + str(if_down))
        
        # have a sleep to allow time for wpa_supplicant to exit?
        import time
        time.sleep(5)
        
        if_up_cmd = "sudo ifup " + str(self.wlan_if_name)
        
        if self.debug:
            print("if up command:")
            print(if_up_cmd)
            
        try:
            if_up = subprocess.check_output(if_up_cmd, stderr=subprocess.STDOUT, shell=True)
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
            print (if_up)
            
        self.file_logger.error("sudo ifup output: " + str(if_up))
        
        return True

    def get_ssid(self):
        return self.ssid
    
    def get_bssid(self):
        return self.bssid
    
    def get_freq(self):
        return self.freq
    
    def get_bit_rate(self):
        return self.bit_rate
    
    def get_signal_level(self):
        return self.signal_level

    def get_ipaddr(self):
        return self.ip_addr
    
    def get_def_gw(self):
        return self.def_gw
