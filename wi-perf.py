#!/usr/bin/python3
# -*- coding: utf-8 -*-
 
from __future__ import print_function
import time
import datetime
import subprocess
from socket import gethostbyname
import os
import re
import sys
import configparser
import csv
import os.path
import logging
import json
#import unicodecsv as csv

# our local modules...
from modules.ooklaspeedtest import ooklaspeedtest
from modules.wirelessadapter import *
from modules.pinger import *
from modules.filelogger import *
from modules.iperf3_tester import tcp_iperf_client_test, udp_iperf_client_test
from modules.dnstester import *
from modules.dhcptester import *

# define useful system files
config_file = os.path.dirname(os.path.realpath(__file__)) + "/config.ini"
log_file = os.path.dirname(os.path.realpath(__file__)) + "/logs/agent.log"

# Enable debugs or create some dummy data for testing
DEBUG = 0
DUMMY_DATA = False

def read_config(debug):
    '''
    Read in the config file variables. 
    '''

    config_vars = {}
    
    config = configparser.ConfigParser()
    config_file = os.path.dirname(os.path.realpath(__file__)) + "/config.ini"
    config.read(config_file)

    # TODO: add checking logic for values in config.ini file

    ### Get general config params
    # WLAN interface name
    config_vars['wlan_if'] = config.get('General', 'wlan_if')
    # Get platform architecture
    config_vars['platform'] = config.get('General', 'platform')
    # format of output data (csv/json)
    config_vars['data_format'] = config.get('General', 'data_format')
    # directory where data dumped
    config_vars['data_dir'] = config.get('General', 'data_dir')
      
    if debug:    
        print("Platform = {}".format(config_vars.get('General', 'platform')))

    ### Get Speedtest config params
    config_vars['speedtest_enabled'] = config.get('Speedtest', 'enabled')
    config_vars['speedtest_data_file'] = config.get('Speedtest', 'speedtest_data_file')

    ### Get Ping config params
    config_vars['ping_enabled'] = config.get('Ping_Test', 'enabled')
    config_vars['ping_data_file'] = config.get('Ping_Test', 'ping_data_file')
    config_vars['ping_host1'] = config.get('Ping_Test', 'ping_host1')
    config_vars['ping_host2'] = config.get('Ping_Test', 'ping_host2')
    config_vars['ping_host3'] = config.get('Ping_Test', 'ping_host3')
    config_vars['ping_host4'] = config.get('Ping_Test', 'ping_host4')
    config_vars['ping_host5'] = config.get('Ping_Test', 'ping_host5')
    config_vars['ping_count'] = config.get('Ping_Test', 'ping_count')

    ### Get iperf3 tcp test params
    config_vars['iperf3_tcp_enabled'] = config.get('Iperf3_tcp_test', 'enabled')
    config_vars['iperf3_tcp_data_file'] = config.get('Iperf3_tcp_test', 'iperf3_tcp_data_file')
    config_vars['iperf3_tcp_server_hostname'] = config.get('Iperf3_tcp_test', 'server_hostname')
    config_vars['iperf3_tcp_port'] = config.get('Iperf3_tcp_test', 'port')
    config_vars['iperf3_tcp_duration'] = config.get('Iperf3_tcp_test', 'duration')

    ### Get iperf3 udp test params
    config_vars['iperf3_udp_enabled'] = config.get('Iperf3_udp_test', 'enabled')
    config_vars['iperf3_udp_data_file'] = config.get('Iperf3_udp_test', 'iperf3_udp_data_file')
    config_vars['iperf3_udp_server_hostname'] = config.get('Iperf3_udp_test', 'server_hostname')
    config_vars['iperf3_udp_port'] = config.get('Iperf3_udp_test', 'port')
    config_vars['iperf3_udp_duration'] = config.get('Iperf3_udp_test', 'duration')
    config_vars['iperf3_udp_bandwidth'] = config.get('Iperf3_udp_test', 'bandwidth')

    ### Get DNS test params
    config_vars['dns_test_enabled'] = config.get('DNS_test', 'enabled')
    config_vars['dns_data_file'] = config.get('DNS_test', 'dns_data_file')
    config_vars['dns_target1'] = config.get('DNS_test', 'dns_target1')
    config_vars['dns_target2'] = config.get('DNS_test', 'dns_target2')
    config_vars['dns_target3'] = config.get('DNS_test', 'dns_target3')
    config_vars['dns_target4'] = config.get('DNS_test', 'dns_target4')
    config_vars['dns_target5'] = config.get('DNS_test', 'dns_target5')

    ### Get DHCP test params
    config_vars['dhcp_test_enabled'] = config.get('DHCP_test', 'enabled')
    config_vars['dhcp_data_file'] = config.get('DHCP_test', 'dhcp_data_file')

    # Figure out our machine_id (provides unique device id if required)
    machine_id = subprocess.check_output("cat /etc/machine-id", shell=True).decode()
    config_vars['machine_id'] = machine_id.strip()
    
    if debug:    
        print("Machine ID = " + config_vars['machine_id'])
   
    return config_vars


def send_results_to_csv(data_file, dict_data, column_headers, file_logger, debug):

    try:
        if os.path.exists(data_file):
            with open(data_file, 'a') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=column_headers)
                writer.writerow(dict_data)
        else:
            with open(data_file, 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=column_headers)
                writer.writeheader()
                writer.writerow(dict_data)
    except IOError as err:
        file_logger.error("CSV I/O error: {}".format(err))

def send_results_to_json(data_file, dict_data, file_logger, debug):

    try:
        # change write/append mode depending on whether data file exists
        file_mode = 'w'
        if os.path.exists(data_file):
            file_mode = 'a'

        with open(data_file, file_mode) as json_file:
            json.dump(dict_data, json_file)
    except IOError:
        file_logger.error("JSON I/O error: {}".format(err))

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
        column_headers = ['timestamp', 'server_name', 'ping_time', 'download_rate', 'upload_rate', 'ssid', 'bssid', 'freq', 'bit_rate', 'signal_level', 'tx_retries', 'ip_address']
        
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
        results_dict['tx_retries'] = int(adapter.get_tx_retries())
        results_dict['ip_address'] = str(adapter.get_ipaddr())
        
        results_dict['timestamp'] = int(time.time())

        # dump the results 
        if config_vars['data_format'] == 'csv':
            data_file = "{}/{}.csv".format(config_vars['data_dir'], config_vars['speedtest_data_file'])
            send_results_to_csv(data_file, results_dict, column_headers, file_logger, DEBUG)
        else:
            data_file = "{}/{}.json".format(config_vars['data_dir'], config_vars['speedtest_data_file'])
            send_results_to_json(data_file, results_dict, file_logger, DEBUG)

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

        ping_host1 = config_vars['ping_host1']
        ping_host2 = config_vars['ping_host2']
        ping_host3 = config_vars['ping_host3']
        ping_host4 = config_vars['ping_host4']
        ping_host5 = config_vars['ping_host5']
        ping_hosts = [ping_host1, ping_host2, ping_host3, ping_host4, ping_host5]

        ping_count = config_vars['ping_count']

        # define colum headers for CSV
        column_headers = ['timestamp', 'ping_index', 'ping_host', 'pkts_tx', 'pkts_rx', 'percent_loss', 'test_time', 'rtt_min', 'rtt_avg', 'rtt_max', 'rtt_mdev']
            
        # initial ping to populate arp cache and avoid arp timeput for first test ping
        for ping_host in ping_hosts:
            if ping_host == '':
                continue
            else:
                # check for def_gw keyword
                if ping_host == 'def_gw':
                    ping_host = adapter.get_def_gw()
                
                ping_obj.ping_host(ping_host, 1)
            
        # ping test
        ping_index = 0
        for ping_host in ping_hosts:
            ping_index += 1

            if ping_host == '':
                    continue
            else:
                # check for def_gw keyword
                if ping_host == 'def_gw':
                    ping_host = adapter.get_def_gw()

                ping_result = ping_obj.ping_host(ping_host, ping_count)

            results_dict = {}
                
            # ping results
            if ping_result:
                results_dict['timestamp'] = int(time.time())
                results_dict['ping_index'] =  ping_index
                results_dict['ping_host'] =  ping_result['host']
                results_dict['pkts_tx'] =  ping_result['pkts_tx']
                results_dict['pkts_rx'] =  ping_result['pkts_rx']
                results_dict['percent_loss'] =  ping_result['pkt_loss']
                results_dict['test_time'] =  ping_result['test_time']
                results_dict['rtt_min'] =  ping_result['rtt_min']
                results_dict['rtt_avg'] =  ping_result['rtt_avg']
                results_dict['rtt_max'] =  ping_result['rtt_max']
                results_dict['rtt_mdev'] =  ping_result['rtt_mdev']

                # dump the results 
                if config_vars['data_format'] == 'csv':
                    data_file = "{}/{}.csv".format(config_vars['data_dir'], config_vars['ping_data_file'])
                    send_results_to_csv(data_file, results_dict, column_headers, file_logger, DEBUG)
                else:
                    data_file = "{}/{}.json".format(config_vars['data_dir'], config_vars['ping_data_file'])
                    send_results_to_json(data_file, results_dict, file_logger, DEBUG)

                file_logger.info("Ping test ended.")

                if DEBUG:
                    print("Main: Ping test results:")
                    print(ping_result)

            else:
                file_logger.error("Ping test failed.")

    else:
        file_logger.info("Ping test not enabled in config file, bypassing this test...")
    
    ###################################
    # Run iperf3 tcp test (if enabled)
    ###################################
    if config_vars['iperf3_tcp_enabled'] == 'yes':

        file_logger.info("Starting iperf3 tcp test...")

        duration = int(config_vars['iperf3_tcp_duration'])
        port = int(config_vars['iperf3_tcp_port'])
        server_hostname = config_vars['iperf3_tcp_server_hostname']

        result = tcp_iperf_client_test(file_logger, server_hostname, duration=duration, port=port, debug=False)

        if result.error == None:

            results_dict = {}
            
            column_headers = ['timestamp', 'sent_mbps', 'received_mbps', 'sent_bytes', 'received_bytes', 'retransmits']

            results_dict['timestamp'] = int(time.time())
            results_dict['sent_mbps'] =  result.sent_Mbps
            results_dict['received_mbps']   =  result.received_Mbps
            results_dict['sent_bytes'] =  result.sent_bytes
            results_dict['received_bytes'] =  result.received_bytes
            results_dict['retransmits'] =  result.retransmits

            # drop abbreviated results in log file
            file_logger.info("Iperf3 tcp results - rx_mbps: {}, tx_bps: {}, retransmits: {}".format(results_dict['received_mbps'], results_dict['sent_mbps'], results_dict['retransmits']))

            # dump the results 
            if config_vars['data_format'] == 'csv':
                data_file = "{}/{}.csv".format(config_vars['data_dir'], config_vars['iperf3_tcp_data_file'])
                send_results_to_csv(data_file, results_dict, column_headers, file_logger, DEBUG)
            else:
                data_file = "{}/{}.json".format(config_vars['data_dir'], config_vars['iperf3_tcp_data_file'])
                send_results_to_json(data_file, results_dict, file_logger, DEBUG)

            file_logger.info("Iperf3 tcp test ended.")

        else:
            file_logger.error("Error with iperf3 tcp test: {}".format(result.error))

    
    else:
        file_logger.info("Iperf3 tcp test not enabled in config file, bypassing this test...")
    
    ###################################
    # Run iperf3 udp test (if enabled)
    ###################################
    if config_vars['iperf3_udp_enabled'] == 'yes':

        file_logger.info("Starting iperf3 udp test...")

        duration = int(config_vars['iperf3_udp_duration'])
        port = int(config_vars['iperf3_udp_port'])
        server_hostname = config_vars['iperf3_udp_server_hostname']
        bandwidth = int(config_vars['iperf3_udp_bandwidth'])

        result = udp_iperf_client_test(file_logger, server_hostname, duration=duration, port=port, bandwidth=bandwidth, debug=False)

        if result.error == None:

            results_dict = {}
            
            column_headers = ['timestamp', 'bytes', 'mbps', 'jitter_ms', 'packets', 'lost_packets', 'lost_percent']

            results_dict['timestamp'] = int(time.time())
            results_dict['bytes'] =  result.bytes
            results_dict['mbps']   =  result.Mbps
            results_dict['jitter_ms'] =  result.jitter_ms
            results_dict['packets'] =  result.packets
            results_dict['lost_packets'] =  result.lost_packets
            results_dict['lost_percent'] =  result.lost_percent

            # drop abbreviated results in log file
            file_logger.info("Iperf3 udp results - mbps: {}, packets: {}, lost_packets: {}, lost_percent: {}".format(results_dict['mbps'], results_dict['packets'], results_dict['lost_packets'], results_dict['lost_percent']))

            # dump the results 
            if config_vars['data_format'] == 'csv':
                data_file = "{}/{}.csv".format(config_vars['data_dir'], config_vars['iperf3_udp_data_file'])
                send_results_to_csv(data_file, results_dict, column_headers, file_logger, DEBUG)
            else:
                data_file = "{}/{}.json".format(config_vars['data_dir'], config_vars['iperf3_udp_data_file'])
                send_results_to_json(data_file, results_dict, file_logger, DEBUG)

            file_logger.info("Iperf3 udp test ended.")

        else:
            file_logger.error("Error with iperf3 udp test: {}".format(result.error))

    
    else:
        file_logger.info("Iperf3 udp test not enabled in config file, bypassing this test...")
    
    ###################################
    # Run DNS lookup tests (if enabled)
    ###################################
    if config_vars['dns_test_enabled'] == 'yes':

        file_logger.info("Starting DNS tests...")

        dns_targets = [ config_vars['dns_target1'], config_vars['dns_target2'], config_vars['dns_target3'], config_vars['dns_target4'], config_vars['dns_target5'] ]

        dns_index = 0

        for dns_target in dns_targets:

            dns_index += 1

            # move on to next if no DNS entry data
            if dns_target == '':
                continue

            dns_obj = DnsTester(file_logger, platform = platform, debug = DEBUG)

            dns_result = dns_obj.dns_single_lookup(dns_target)

            if dns_result:
    
                column_headers = ['timestamp', 'dns_index', 'dns_target', 'lookup_time']

                # summarise result for log
                result_str = ' {}: {}ms'.format(dns_target, dns_result)

                # drop abbreviated results in log file
                file_logger.info("DNS results: {}".format(result_str))

                results_dict = { 
                        'timestamp':int(time.time()),
                        'dns_index': dns_index,
                        'dns_target': dns_target, 
                        'lookup_time': dns_result
                }

                # dump the results 
                if config_vars['data_format'] == 'csv':
                    data_file = "{}/{}.csv".format(config_vars['data_dir'], config_vars['dns_data_file'])
                    send_results_to_csv(data_file, results_dict, column_headers, file_logger, DEBUG)
                else:
                    data_file = "{}/{}.json".format(config_vars['data_dir'], config_vars['dns_data_file'])
                    send_results_to_json(data_file, results_dict, file_logger, DEBUG)

                file_logger.info("DNS test ended.")

            else:
                file_logger.error("DNS test error - no results (check logs)")

    
    else:
        file_logger.info("DNS test not enabled in config file, bypassing this test...")
        
    
    #####################################
    # Run DHCP renewal test (if enabled)
    #####################################
    if config_vars['dhcp_test_enabled'] == 'yes':

        file_logger.info("Starting DHCP renewal test...")

        dhcp_obj = DhcpTester(file_logger, platform = platform, debug = DEBUG)

        renewal_result = dhcp_obj.dhcp_renewal(wlan_if)

        if renewal_result:
 
            column_headers = ['timestamp', 'dhcp_renewal_time']

            results_dict = { 
                    'timestamp':int(time.time()),
                    'dhcp_renewal_time': renewal_result, 
            }

            # dump the results 
            if config_vars['data_format'] == 'csv':
                data_file = "{}/{}.csv".format(config_vars['data_dir'], config_vars['dhcp_data_file'])
                send_results_to_csv(data_file, results_dict, column_headers, file_logger, DEBUG)
            else:
                data_file = "{}/{}.json".format(config_vars['data_dir'], config_vars['dhcp_data_file'])
                send_results_to_json(data_file, results_dict, file_logger, DEBUG)

            file_logger.info("DHCP test ended.")

        else:
            file_logger.error("DHCP test error - no results (check logs)")

    
    else:
        file_logger.info("DHCP test not enabled in config file, bypassing this test...")
###############################################################################
# End main
###############################################################################
    
if __name__ == "__main__":
    main()
