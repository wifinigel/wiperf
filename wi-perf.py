#!/usr/bin/python
# -*- coding: latin-1 -*-
 
from __future__ import print_function
import time
import datetime
import subprocess
from socket import gethostbyname
from ooklaspeedtest import ooklaspeedtest
import os
import re
import sys
import ConfigParser
import csv
import os.path
import logging
import csv

# our local modules...
from wirelessadapter import *
from pinger import *
from filelogger import *

# define useful system files
config_file = os.path.dirname(os.path.realpath(__file__)) + "/config.ini"
log_file = os.path.dirname(os.path.realpath(__file__)) + "/agent.log"

# Enable debugs or create some dummy data for testing
DEBUG = 0
DUMMY_DATA = False

def read_config(debug):
    '''
    Read in the config file variables. 
    '''

    config_vars = {}
    
    config = ConfigParser.SafeConfigParser()
    config_file = os.path.dirname(os.path.realpath(__file__)) + "/config.ini"
    config.read(config_file)

    ### Get general config params
    # WLAN interface name
    config_vars['wlan_if'] = config.get('General', 'wlan_if')
    # Get platform architecture
    config_vars['platform'] = config.get('General', 'platform')
      
    if debug:    
        print("Platform = {}".format(config_vars.get('General', 'platform')))

    ### Get Speedtest config params
    config_vars['speedtest_enabled'] = config.get('Speedtest', 'enabled')
    config_vars['speedtest_csv_file'] = config.get('Speedtest', 'speedtest_csv_file')

    ### Get Ping config params
    config_vars['ping_enabled'] = config.get('Ping_Test', 'enabled')
    config_vars['ping_csv_file'] = config.get('Ping_Test', 'ping_csv_file')
    config_vars['ping_host'] = config.get('Ping_Test', 'ping_host')
    config_vars['ping_count'] = config.get('Ping_Test', 'ping_count')



    # Figure out our machine_id
    machine_id = subprocess.check_output("cat /etc/machine-id", shell=True)
    config_vars['machine_id'] = machine_id.strip()
    
    if debug:    
        print("Machine ID = " + config_vars['machine_id'])
   
    return config_vars


def send_results_to_csv(csv_file, dict_data, column_headers, file_logger, debug):

    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=column_headers)
            #writer.writeheader()
            writer.writerow(dict_data)
    except IOError:
        file_logger.error("CSV I/O error") 

def bounce_error_exit(adapter, file_logger, debug=False): 
    '''
    Log an error before bouncing the wlan interface and then exiting as we have an unrecoverable error with the network connection
    '''
    import sys
    
    file_logger.error("Bouncing WLAN interface")
    
    adapter.bounce_wlan_interface()
    
    file_logger.error("Exiting...")
    
    sys.exit()   
    
    
###############################################################################
# Main
###############################################################################
    
def main():

    # read in our local config file (content in dictionary: config_vars)
    
    config_vars = read_config(DEBUG)
    
    wlan_if = config_vars['wlan_if']
    platform = config_vars['platform']
  
    ###################################
    # File logger
    ###################################
        
    # set up our error_log file & initialize
    file_logger = FileLogger(log_file)
    file_logger.info("Starting logging...")
    
    # get wireless info
    adapter = WirelessAdapter(wlan_if, file_logger, platform=platform, debug=DEBUG)   

    # if we have no network connection (i.e. no bssid), no point in proceeding...
    if adapter.get_wireless_info() == False:
        file_logger.error("Unable to get wireless info due to failure with ifconfig command")
        bounce_error_exit(adapter, file_logger, DEBUG) # exit here
        
    if adapter.get_bssid() == 'NA':
        file_logger.error("Problem with wireless connection: not associated to network")
        file_logger.error("Attempting to recover by bouncing wireless interface...")
        bounce_error_exit(adapter, file_logger, DEBUG) # exit here
    
    # if we have no IP address, no point in proceeding...
    if adapter.get_adapter_ip() == False:
        file_logger.error("Unable to get wireless adapter IP info")
        bounce_error_exit(adapter, file_logger, DEBUG) # exit here
    
    '''
    if adapter.get_route_info() == False:
        file_logger.error("Unable to get wireless adapter route info - maybe you have multiple interfaces enabled that are stopping the wlan interface being used?")
        bounce_error_exit(adapter, file_logger, DEBUG) # exit here
    '''
    if adapter.get_ipaddr() == 'NA':
        file_logger.error("Problem with wireless connection: no valid IP address")
        file_logger.error("Attempting to recover by bouncing wireless interface...")
        bounce_error_exit(adapter, file_logger, DEBUG) # exit here
    
    # final connectivity check: see if we can resolve an address 
    # (network connection and DNS must be up)
    try:
        gethostbyname('bbc.co.uk')
    except Exception as ex:
        file_logger.error("DNS seems to be failing, bouncing wireless interface. Err msg: {}".format(ex))
        bounce_error_exit(adapter, file_logger,  DEBUG) # exit here

    #############################
    # Run speedtest (if enabled)
    #############################
    if config_vars['speedtest_enabled'] == 'yes':

        file_logger.info("Starting speedtest...")

        speedtest_results = ooklaspeedtest(file_logger)
        
        if DEBUG:
            print("Main: Speedtest results:")
            print(speedtest_results)
        
        # hold all results in one place
        results_dict = {}

        # define column headers
        column_headers = ['timestamp', 'server_name', 'ping_time', 'download_rate', 'upload_rate', 'ssid', 'bssid', 'freq', 'bit_rate', 'signal_level', 'ip_address']
        
        # speedtest results
        results_dict['ping_time'] = int(speedtest_results['ping_time'])
        results_dict['download_rate'] = float(speedtest_results['download_rate'])
        results_dict['upload_rate'] = float(speedtest_results['upload_rate'])
        results_dict['server_name'] = str(speedtest_results['server_name'])
        
        results_dict['ssid'] = str(adapter.get_ssid())
        results_dict['bssid'] = str(adapter.get_bssid())
        results_dict['freq'] = str(adapter.get_freq())
        results_dict['bit_rate'] = float(adapter.get_bit_rate())
        results_dict['signal_level'] = int(adapter.get_signal_level())
        results_dict['ip_address'] = str(adapter.get_ipaddr())
        
        results_dict['timestamp'] = int(time.time())

        # dump the results to csv
        send_results_to_csv(config_vars['speedtest_csv_file'], results_dict, column_headers, file_logger, DEBUG)

        file_logger.info("Speedtest ended.")

    else:
        file_logger.info("Speedtest not enabled in config file, bypassing this test...")

    #############################
    # Run ping test (if enabled)
    #############################
    if config_vars['ping_enabled'] == 'yes':

        file_logger.info("Starting ping test...")
          
        # run ping test
        ping_obj = Pinger(file_logger, platform = platform, debug = DEBUG)

        ping_host = config_vars['ping_host']
        ping_count = config_vars['ping_count']

        # define colum headers for CSV
        column_headers = ['ping_host', 'pkts_tx', 'pkts_rx', 'percent_loss', 'test_time', 'rtt_min', 'rtt_avg', 'rtt_max', 'rtt_mdev']
            
        # initial ping to populate arp cache and avoid arp timeput for first test ping
        ping_obj.ping_host(ping_host, 1)
            
        # ping test
        ping_result = ping_obj.ping_host(ping_host, ping_count)

        results_dict = {}
            
        # ping results
        if ping_result:
            results_dict['ping_host'] =  ping_result['host']
            results_dict['pkts_tx'] =  ping_result['pkts_tx']
            results_dict['pkts_rx'] =  ping_result['pkts_rx']
            results_dict['percent_loss'] =  ping_result['pkt_loss']
            results_dict['test_time'] =  ping_result['test_time']
            results_dict['rtt_min'] =  ping_result['rtt_min']
            results_dict['rtt_avg'] =  ping_result['rtt_avg']
            results_dict['rtt_max'] =  ping_result['rtt_max']
            results_dict['rtt_mdev'] =  ping_result['rtt_mdev']

            # dump the results to csv
            send_results_to_csv(config_vars['ping_csv_file'], results_dict, column_headers, file_logger, DEBUG)

            file_logger.info("Ping test ended.")

            if DEBUG:
                print("Main: Ping test results:")
                print(ping_result)

        else:
            file_logger.error("Ping test failed.")

    else:
        file_logger.info("Ping test not enabled in config file, bypassing this test...")
        
###############################################################################
# End main
###############################################################################
    
if __name__ == "__main__":
    main()
