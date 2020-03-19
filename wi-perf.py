#!/usr/bin/python3
# -*- coding: utf-8 -*-

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
import requests

# our local modules...
from modules.ooklaspeedtest import ooklaspeedtest
from modules.wirelessadapter import *
from modules.pinger import *
from modules.filelogger import *
from modules.heclogger import *
from modules.iperf3_tester import tcp_iperf_client_test, udp_iperf_client_test
from modules.dnstester import *
from modules.httptester import *
from modules.dhcptester import *
from modules.fieldchecker import *

# define useful system files
config_file = os.path.dirname(os.path.realpath(__file__)) + "/config.ini"
log_file = os.path.dirname(os.path.realpath(__file__)) + "/logs/agent.log"
lock_file = '/tmp/wiperf.lock'
mode_active = os.path.dirname(os.path.realpath(__file__)) + "/wiperf_mode.on"
status_file = '/tmp/wiperf_status.txt'
watchdog_file = '/tmp/wiperf.watchdog'
bounce_file = '/tmp/wiperf.bounce'
check_cfg_file = '/tmp/wiperf.cfg'

# Enable debugs or create some dummy data for testing
DEBUG = 0
DUMMY_DATA = False

config_vars = {}

###################################
# File logger
###################################

# set up our error_log file & initialize
file_logger = FileLogger(log_file)
file_logger.info("*****************************************************")
file_logger.info(" Starting logging...")
file_logger.info("*****************************************************")


def read_config(debug):
    '''
    Read in the config file variables. 
    '''

    global config_vars

    config = configparser.ConfigParser()
    config_file = os.path.dirname(os.path.realpath(__file__)) + "/config.ini"
    config.read(config_file)

    # TODO: add checking logic for values in config.ini file

    # Get general config params
    gen_sect = config['General']
    # WLAN interface name
    config_vars['wlan_if'] = gen_sect.get('wlan_if', 'wlan0')
    # Interface name to send mgt traffic over (default wlan0)
    config_vars['mgt_if'] = gen_sect.get('mgt_if', 'wlan0')
    # Get platform architecture
    config_vars['platform'] = gen_sect.get('platform', 'wlanpi')
    # format of output data (csv/json)
    config_vars['data_format'] = gen_sect.get('data_format', 'json')
    # directory where data dumped
    config_vars['data_dir'] = gen_sect.get('data_dir')
    # data transport
    config_vars['data_transport'] = gen_sect.get('data_transport', 'hec')
    # host where to send logs
    config_vars['data_host'] = gen_sect.get('data_host')
    # host port
    config_vars['data_port'] = gen_sect.get('data_port', '8088')
    # Splunk HEC token
    config_vars['splunk_token'] = gen_sect.get('splunk_token')

    # test cycle timing parameters
    config_vars['test_interval'] = gen_sect.get('test_interval', '5')
    config_vars['test_offset'] = gen_sect.get('test_offset', '0')

    # connectivity DNS lookup - site used for initial DNS lookup when assessing if DNS working OK
    config_vars['connectivity_lookup'] = gen_sect.get('connectivity_lookup', 'google.com')


    # unit bouncer - hours at which we'd like to bounce unit (e.g. 00, 04, 08, 12, 16, 20)
    config_vars['unit_bouncer'] = gen_sect.get('unit_bouncer', False)

    # location
    config_vars['location'] = gen_sect.get('location', '')

    # config server details (if supplied)
    config_vars['cfg_filename'] = gen_sect.get('cfg_filename', '')
    config_vars['cfg_url'] = gen_sect.get('cfg_url', '')
    config_vars['cfg_username'] = gen_sect.get('cfg_username', '')
    config_vars['cfg_password'] = gen_sect.get('cfg_password', '')
    config_vars['cfg_token'] = gen_sect.get('cfg_token', '')
    config_vars['cfg_refresh_interval'] = gen_sect.get('cfg_refresh_interval', 1800)

    # do some basic checks that mandatory fields are present
    for field in ['data_host', 'splunk_token']:

        if config_vars[field] == '':
            err_msg = "No value in config.ini for field value: {} - exiting...".format(
                field)
            file_logger.error(err_msg)
            print(err_msg)
            sys.exit()

    if debug:
        print("Platform = {}".format(config_vars.get('General', 'platform')))

    # Get Speedtest config params
    speed_sect = config['Speedtest']
    config_vars['speedtest_enabled'] = speed_sect.get('enabled', 'no')
    config_vars['server_id'] = speed_sect.get('server_id', '')
    config_vars['speedtest_data_file'] = speed_sect.get(
        'speedtest_data_file', '')
    config_vars['http_proxy'] = speed_sect.get('http_proxy', '')
    config_vars['https_proxy'] = speed_sect.get('https_proxy', '')
    config_vars['no_proxy'] = speed_sect.get('no_proxy', '')
    # set env vars if they are specified in the config file
    for proxy_var in ['http_proxy', 'https_proxy', 'no_proxy']:

        if config_vars[proxy_var]:
            os.environ[proxy_var] = config_vars[proxy_var]

    # Get Ping config params
    ping_sect = config['Ping_Test']
    config_vars['ping_enabled'] = ping_sect.get('enabled', 'no')
    config_vars['ping_data_file'] = ping_sect.get('ping_data_file', '')
    config_vars['ping_host1'] = ping_sect.get('ping_host1', '')
    config_vars['ping_host2'] = ping_sect.get('ping_host2', '')
    config_vars['ping_host3'] = ping_sect.get('ping_host3', '')
    config_vars['ping_host4'] = ping_sect.get('ping_host4', '')
    config_vars['ping_host5'] = ping_sect.get('ping_host5', '')
    config_vars['ping_count'] = ping_sect.get('ping_count', '')

    # Get iperf3 tcp test params
    iperft_sect = config['Iperf3_tcp_test']
    config_vars['iperf3_tcp_enabled'] = iperft_sect.get('enabled', 'no')
    config_vars['iperf3_tcp_data_file'] = iperft_sect.get(
        'iperf3_tcp_data_file', '')
    config_vars['iperf3_tcp_server_hostname'] = iperft_sect.get(
        'server_hostname', '')
    config_vars['iperf3_tcp_port'] = iperft_sect.get('port', '')
    config_vars['iperf3_tcp_duration'] = iperft_sect.get('duration', '')

    # Get iperf3 udp test params
    iperfu_sect = config['Iperf3_udp_test']
    config_vars['iperf3_udp_enabled'] = iperfu_sect.get('enabled', 'no')
    config_vars['iperf3_udp_data_file'] = iperfu_sect.get(
        'iperf3_udp_data_file', '')
    config_vars['iperf3_udp_server_hostname'] = iperfu_sect.get(
        'server_hostname', '')
    config_vars['iperf3_udp_port'] = iperfu_sect.get('port', '')
    config_vars['iperf3_udp_duration'] = iperfu_sect.get('duration', '')
    config_vars['iperf3_udp_bandwidth'] = iperfu_sect.get('bandwidth', '')

    # Get DNS test params
    dns_sect = config['DNS_test']
    config_vars['dns_test_enabled'] = dns_sect.get('enabled', 'no')
    config_vars['dns_data_file'] = dns_sect.get('dns_data_file', '')
    config_vars['dns_target1'] = dns_sect.get('dns_target1', '')
    config_vars['dns_target2'] = dns_sect.get('dns_target2', '')
    config_vars['dns_target3'] = dns_sect.get('dns_target3', '')
    config_vars['dns_target4'] = dns_sect.get('dns_target4', '')
    config_vars['dns_target5'] = dns_sect.get('dns_target5', '')

    # Get http test params
    http_sect = config['HTTP_test']
    config_vars['http_test_enabled'] = http_sect.get('enabled', 'no')
    config_vars['http_data_file'] = http_sect.get('http_data_file', '')
    config_vars['http_target1'] = http_sect.get('http_target1', '')
    config_vars['http_target2'] = http_sect.get('http_target2', '')
    config_vars['http_target3'] = http_sect.get('http_target3', '')
    config_vars['http_target4'] = http_sect.get('http_target4', '')
    config_vars['http_target5'] = http_sect.get('http_target5', '')

    # Get DHCP test params
    dhcp_sect = config['DHCP_test']
    config_vars['dhcp_test_enabled'] = dhcp_sect.get('enabled', 'no')
    config_vars['dhcp_test_mode'] = dhcp_sect.get('mode', 'passive')
    config_vars['dhcp_data_file'] = dhcp_sect.get('dhcp_data_file', '')

    '''
    # Check all entered config.ini values to see if valid
    for key in config_vars: 

        field = key
        value = config_vars[field]   

        if FieldCheck(field, value, DEBUG) == False:
            err_msg = "Config.ini field error: {} (value = [{}])".format(field, value)
            file_logger.error(err_msg)
            print(err_msg + "...exiting")
            sys.exit()

    # Figure out our machine_id (provides unique device id if required)
    machine_id = subprocess.check_output("cat /etc/machine-id", stderr=subprocess.STDOUT, shell=True).decode()
    config_vars['machine_id'] = machine_id.strip()

    if debug:    
        print("Machine ID = " + config_vars['machine_id'])
    '''

    return config_vars


def send_results_to_csv(data_file, dict_data, column_headers, file_logger, debug, delete_data_file=True):

    try:
        # if False:
        if os.path.exists(data_file) and (delete_data_file == False):
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


def send_results_to_json(data_file, dict_data, file_logger, debug, delete_data_file=True):

    try:
        # change write/append mode depending on whether data file exists
        file_mode = 'w'
        if os.path.exists(data_file) and (delete_data_file == False):
            file_mode = 'a'

        with open(data_file, file_mode) as json_file:
            json.dump(dict_data, json_file)
    except IOError as err:
        file_logger.error("JSON I/O error: {}".format(err))


def send_results_to_hec(host, token, port, dict_data, file_logger, source, debug=False):

    file_logger.info("Sending event to HEC: {} (dest host: {}, dest port: {})".format(
        source, host, port))
    HecLogger(host, token, port, dict_data, source, file_logger, debug)


def send_results(results_dict, column_headers, data_file, test_name, file_logger, debug, delete_data_file=False):

    global config_vars

    # dump the results to appropriate destination

    # Check if we are using the Splunk HEC (https transport)
    if config_vars['data_transport'] == 'hec':
        file_logger.info(
            "HEC update: {}, source={}".format(data_file, test_name))
        send_results_to_hec(config_vars['data_host'], config_vars['splunk_token'], config_vars['data_port'],
                            results_dict, file_logger, data_file, debug)
    # Create files if we are using the Splunk universal forwarder
    elif config_vars['data_transport'] == 'forwarder':

        # CSV file format for forwarder
        if config_vars['data_format'] == 'csv':
            data_file = "{}/{}.csv".format(config_vars['data_dir'], data_file)
            send_results_to_csv(data_file, results_dict, column_headers,
                                file_logger, debug, delete_data_file=delete_data_file)
        # JSON format for the forwarder
        elif config_vars['data_format'] == 'json':
            data_file = "{}/{}.json".format(config_vars['data_dir'], data_file)
            send_results_to_json(
                data_file, results_dict, file_logger, debug, delete_data_file=delete_data_file)
        else:
            file_logger.info("Unknown file format type in config file: {}".format(
                config_vars['data_format']))
            exit()
    # Transport type which is not know has been configured in the ini file
    else:
        file_logger.info("Unknown transport type in config file: {}".format(
            config_vars['data_transport']))
        exit()

    return True


def read_lock_file(filename, file_logger):

    try:
        with open(lock_file, 'r') as lockf:
            lock_timestamp = lockf.read()
        return lock_timestamp
    except Exception as ex:
        file_logger.error("Issue reading lock file: {}, exiting...".format(ex))
        sys.exit()


def write_lock_file(filename, file_logger):
    try:
        time_now = int(time.time())
        with open(lock_file, 'w') as lockf:
            lockf.write(str(time_now))
        return True
    except Exception as ex:
        file_logger.error("Issue writing lock file: {}, exiting...".format(ex))
        sys.exit()


def delete_lock_file(lock_file, file_logger):
    try:
        os.remove(lock_file)
        file_logger.info("removing lock file")
        return True
    except Exception as ex:
        file_logger.error(
            "Issue deleting lock file: {}, exiting...".format(ex))
        sys.exit()


def bounce_error_exit(adapter, file_logger, debug=False):
    '''
    Log an error before bouncing the wlan interface and then exiting as we have an unrecoverable error with the network connection
    '''
    import sys

    file_logger.error(
        "Attempting to recover by bouncing wireless interface...")
    file_logger.error("Bouncing WLAN interface")
    adapter.bounce_wlan_interface()
    file_logger.error("Bounce completed. Exiting script.")

    # clean up lock file & exit
    delete_lock_file(lock_file, file_logger)
    sys.exit()

####################################
# config server
####################################
def read_remote_cfg(file_logger):
    """
    Pull the remote cfg file if refresh time expired or on first boot
    """

    cfg_file_url = config_vars['cfg_url']
    cfg_token = config_vars['cfg_token']
    cfg_username = config_vars['cfg_username']
    cfg_password = config_vars['cfg_password']
    cfg_text = ''
    
    # if we use a token, we need to set user/pwd to be token
    if cfg_token:
        cfg_username = cfg_token
        cfg_password = cfg_token
    
    file_logger.info("Trying to pull config file from : {}".format(cfg_file_url))
    try:
        response = requests.get(cfg_file_url, auth=(cfg_username, cfg_password), timeout=5)
        if response.status_code == 200:
           cfg_text = response.text
        file_logger.info("Config file pulled OK.")
    except Exception as err:
        file_logger.error("Config file pull error:")
        file_logger.error("HTTP get error: {}".format(err))
        return False

    if cfg_text:
        file_logger.info("Writing pulled config file...")
        try:   
            with open(config_file, 'w') as f:
                f.write(cfg_text)
            file_logger.info("Config file written OK.")
            write_cfg_timestamp(check_cfg_file, file_logger)
            return True
        except Exception as ex:
            file_logger.error("Config file write error:")
            file_logger.error("Issue writing cfg timestamp file: {}".format(ex))
            return False
    else:
        file_logger.info("No data detected in cfg file, nothing written to file (check file URL)")
        return False

def write_cfg_timestamp(check_cfg_file, file_logger):
    """
    Write current timestamp to cfg timestamp file
    """
    
    time_now = str(int(time.time()))
    
    file_logger.info("Writing current time to cfg timestamp file...")
    try:   
        with open(check_cfg_file, 'w') as f:
            f.write(time_now)
        file_logger.info("Written OK.")
        return True
    except Exception as ex:
        file_logger.error("Issue writing cfg timestamp file: {}".format(ex))
        return False


def check_last_cfg_read(check_cfg_file, file_logger):
    """
    Read timestamp from cfg timestamp file and force pull of remote cfg file if required
    """

    time_now = int(time.time())
    last_read_time = 0

    file_logger.info("Checking cfg last-read timestamp...")
    try:
        with open(check_cfg_file) as f:
            last_read_time = f.read()
        file_logger.info("Last read timestamp: {}".format(last_read_time))
    except FileNotFoundError:
        # file does not exist, create & write timestamp
        file_logger.info("Timestamp file does not exist, creating...")
        write_cfg_timestamp(check_cfg_file, file_logger)
    except Exception as e:
        file_logger.info("File read error: {}".format(e))
        return False
    
    # if config file not read in last 30 mins, pull cfg file
    file_logger.info("Checking time diff, time now: {}, last read time: {}".format(time_now, last_read_time))
    if (time_now - int(last_read_time)) >  int(config_vars['cfg_refresh_interval']):
        file_logger.info("Time to read remote cfg file...")
        return read_remote_cfg(file_logger)
    else:
        file_logger.info("Not time to read remote cfg file.")
        return False

####################################
# Unit bouncer
####################################
def check_bounce_file(bounce_file, file_logger):

    if os.path.exists(bounce_file):
        return True

    return False


def read_bounce_file(bounce_file, file_logger):

    try:
        with open(bounce_file, 'r') as bouncef:
            hour = bouncef.read()
        return hour
    except Exception as ex:
        file_logger.error(
            "Issue reading bounce file: {}, exiting...".format(ex))
        sys.exit()


def write_bounce_file(bounce_file, hour, file_logger):

    try:
        with open(bounce_file, 'w') as bouncef:
            bouncef.write(str(hour))
        return True
    except Exception as ex:
        file_logger.error(
            "Issue writing bounce file: {}, exiting...".format(ex))
        sys.exit()


def check_for_bounce(bounce_file, file_logger):

    # split out the hours we need to bounce the interface
    bounce_hours = config_vars['unit_bouncer'].split(",")
    bounce_hours = [i.strip() for i in bounce_hours]

    # get current time and extract hour
    now = datetime.datetime.now()
    current_hour = '{:02d}'.format(now.hour)

    # check if we have a bounce file that shows time of last bounce
    if check_bounce_file(bounce_file, file_logger):

        last_bounce = read_bounce_file(bounce_file, file_logger)

        # is it time to bounce?
        if current_hour in bounce_hours:

            file_logger.info("Time to bounce unit?")

            # possibly time to bounce, have we already bounced?
            if last_bounce != current_hour:

                file_logger.info("Yes, bouncing unit (reboot)")

                # it's time to reboot
                write_bounce_file(bounce_file, current_hour, file_logger)

                try:
                    reboot_output = subprocess.check_output(
                        'sudo /sbin/reboot', stderr=subprocess.STDOUT, shell=True).decode()
                    file_logger.info("Reboot output: {}".format(reboot_output))
                except subprocess.CalledProcessError as exc:
                    output = exc.output.decode()
                    file_logger.error(
                        "Reboot command had issue: {}.".format(str(output)))
            else:
                file_logger.info("No.")

    else:

        # bounce file does not exist, create it with current hour to stop bouncing
        file_logger.info("Creating bounce file.")
        write_bounce_file(bounce_file, str(current_hour), file_logger)


def check_route_to_dest(ip_address, file_logger):

    # If ip address is a hostname rather than an IP, do a lookup and substitute IP
    if re.search(r'[a-z]|[A-Z]', ip_address):
        hostname = ip_address
        # watch out for DNS Issues
        try:
            ip_address = gethostbyname(hostname)
            file_logger.info(
                "DNS hostname lookup : {}. Result: {}".format(hostname, ip_address))
        except Exception as ex:
            file_logger.error(
                "Issue looking up host {} (DNS Issue?): {}".format(hostname, ex))
            return False

    ip_route_cmd = "/bin/ip route show to match " + \
        ip_address + " | head -n 1 | awk '{print $5}'"

    try:
        interface_name = subprocess.check_output(
            ip_route_cmd, stderr=subprocess.STDOUT, shell=True).decode()
        file_logger.info("Checked interface route to : {}. Result: {}".format(
            ip_address, interface_name.strip()))
        return interface_name.strip()
    except subprocess.CalledProcessError as exc:
        output = exc.output.decode()
        file_logger.error("Issue looking up route (route cmd syntax?): {} (command used: {})".format(
            str(output), ip_route_cmd))
        return ''

# write current status msg to file in /tmp for display on FPMS
def write_status_file(text="", status_file=status_file, file_logger=file_logger):

    if text == '':

        # if no text sent, delete file
        if os.path.exists(status_file):
            try:
                os.remove(status_file)
            except Exception as ex:
                file_logger.error("Issue deleting status file: {}.".format(ex))
    else:
        # write status message to file
        try:
            with open(status_file, 'w') as statusf:
                statusf.write(str(text))
        except Exception as ex:
            file_logger.error("Issue writing status file: {}.".format(ex))

    time.sleep(1)
    return True

###################################################
# Watchdog
###################################################
def write_watchdog_count(watchdog_count, watchdog_file=watchdog_file, file_logger=file_logger):

    try:
        with open(watchdog_file, 'w') as watchf:
            watchf.write(str(watchdog_count))
        return True
    except Exception as ex:
        file_logger.error("Issue writing watchdog file: {}.".format(ex))

    return False


def get_watchdog_count(watchdog_file=watchdog_file, file_logger=file_logger):

    if os.path.exists(watchdog_file):
        try:
            with open(watchdog_file, 'r') as watchf:
                watchdog_count = watchf.read()
                return int(watchdog_count)
        except Exception as ex:
            file_logger.error("Issue reading watchdog file: {}.".format(ex))

    return False

# create watchdog file if doesn't exist


def create_watchdog(watchdog_file=watchdog_file, file_logger=file_logger):

    if not os.path.exists(watchdog_file):
        try:
            with open(watchdog_file, 'w') as watchf:
                watchf.write(str('0'))
            return True
        except Exception as ex:
            file_logger.error("Issue creating watchdog file: {}.".format(ex))

    return False

# increment watchdog counter due to issue


def inc_watchdog_count(watchdog_file=watchdog_file, file_logger=file_logger):

    watchdog_count = get_watchdog_count(watchdog_file, file_logger=file_logger)
    watchdog_count += 1
    write_watchdog_count(watchdog_count, watchdog_file,
                         file_logger=file_logger)

    return True

# decrement watchdog counter as test cycle successful


def dec_watchdog_count(watchdog_file=watchdog_file, file_logger=file_logger):

    watchdog_count = get_watchdog_count(watchdog_file, file_logger=file_logger)

    # already zero? Do nothing & return
    if watchdog_count == 0:
        return True

    watchdog_count -= 1
    write_watchdog_count(watchdog_count, watchdog_file,
                         file_logger=file_logger)

    return True

###############################################################################
# Main
###############################################################################
def main():

    global file_logger

    # read in our local config file (content in dictionary: config_vars)
    config_vars = read_config(DEBUG)

    # if we have a config server specified, check to see if it's time
    # to pull the config
    file_logger.info("Checking if we use remote cfg file...")
    if config_vars['cfg_url']:
        
        # if able to get cfg file, re-read params in case updated
        if check_last_cfg_read(check_cfg_file, file_logger):
            config_vars = read_config(DEBUG)
    else:
        file_logger.info("No remote cfg file confgured...using current local ini file.")

    wlan_if = config_vars['wlan_if']
    platform = config_vars['platform']

    # create watchdog if doesn't exist
    create_watchdog()

    # check watchdog count...if higher than 5, time for a reboot
    watchdog_count = get_watchdog_count()
    if watchdog_count > 3:
        file_logger.error("Watchdog count exceeded...rebooting")
        try:
            reboot_output = subprocess.check_output(
                'sudo /sbin/reboot', stderr=subprocess.STDOUT, shell=True).decode()
            file_logger.error("Reboot output: {}".format(reboot_output))
            file_logger.error("Exiting script.")
            sys.exit()
        except subprocess.CalledProcessError as exc:
            output = exc.output.decode()
            file_logger.error(
                "Reboot command had issue: {}.".format(str(output)))

    ###################################
    # Check if script already running
    ###################################
    if os.path.exists(lock_file):
            # read lock file contents & check how old timestamp is..
        file_logger.error("Existing lock file found...")
        lock_timestamp = read_lock_file(lock_file, file_logger)
        inc_watchdog_count()

        # if timestamp older than 10 mins, break lock by
        # creating a new file
        time_now = time.time()
        if (time_now - int(lock_timestamp)) > 540:
            file_logger.error("Existing lock stale, breaking lock...")
            file_logger.error("Current time: {}, lock file time: {}".format(
                time_now, lock_timestamp))
            write_lock_file(lock_file, file_logger)
        else:
            file_logger.error(
                "Exiting due to lock file indicating script running.")
            file_logger.error(
                "(Delete {} if you are sure script not running)".format(lock_file))
            sys.exit()
    else:
        # create lockfile with current timestamp
        file_logger.info("No lock file found. Creating lock file.")
        write_lock_file(lock_file, file_logger)

    #####################
    # get wireless info
    #####################
    file_logger.info("########## wireless connection checks ##########")
    adapter = WirelessAdapter(wlan_if, file_logger,
                              platform=platform, debug=DEBUG)

    # if we have no network connection (i.e. no bssid), no point in proceeding...
    file_logger.info("Checking wireless connection available.")
    if adapter.get_wireless_info() == False:
        file_logger.error(
            "Unable to get wireless info due to failure with ifconfig command")
        inc_watchdog_count()
        bounce_error_exit(adapter, file_logger, DEBUG)  # exit here

    file_logger.info("Checking we're connected to the network")
    if adapter.get_bssid() == 'NA':
        file_logger.error(
            "Problem with wireless connection: not associated to network")
        inc_watchdog_count()
        bounce_error_exit(adapter, file_logger, DEBUG)  # exit here

    file_logger.info("Checking we have an IP address.")
    # if we have no IP address, no point in proceeding...
    if adapter.get_adapter_ip() == False:
        file_logger.error("Unable to get wireless adapter IP info")
        inc_watchdog_count()
        bounce_error_exit(adapter, file_logger, DEBUG)  # exit here

    # TODO: Fix this. Currently breaks when we have Eth & Wireless ports both up
    '''
    if adapter.get_route_info() == False:
        file_logger.error("Unable to get wireless adapter route info - maybe you have multiple interfaces enabled that are stopping the wlan interface being used?")
        bounce_error_exit(adapter, file_logger, DEBUG) # exit here
    '''

    if adapter.get_ipaddr() == 'NA':
        file_logger.error(
            "Problem with wireless connection: no valid IP address")
        inc_watchdog_count()
        bounce_error_exit(adapter, file_logger, DEBUG)  # exit here

    # final connectivity check: see if we can resolve an address
    # (network connection and DNS must be up)
    file_logger.info("Checking we can do a DNS lookup to {}".format(config_vars['connectivity_lookup']))
    try:
        gethostbyname(config_vars['connectivity_lookup'])
    except Exception as ex:
        file_logger.error(
            "DNS seems to be failing, bouncing wireless interface. Err msg: {}".format(ex))
        inc_watchdog_count()
        bounce_error_exit(adapter, file_logger,  DEBUG)  # exit here

    # if we are using hec, make sure we can access the hec network port, otherwise we are wasting our time
    if config_vars['data_transport'] == 'hec':
        file_logger.info("Checking port connection to server {}, port: {}".format(
            config_vars['data_host'], config_vars['data_port']))

        try:
            portcheck_output = subprocess.check_output('/bin/nc -zvw10 {} {}'.format(
                config_vars['data_host'], config_vars['data_port']), stderr=subprocess.STDOUT, shell=True).decode()
            file_logger.info("Port connection to server {}, port: {} checked OK.".format(
                config_vars['data_host'], config_vars['data_port']))
        except subprocess.CalledProcessError as exc:
            output = exc.output.decode()
            file_logger.error(
                "Port check to server failed. Err msg: {} (Exiting...)".format(str(output)))
            inc_watchdog_count()
            delete_lock_file(lock_file, file_logger)
            sys.exit()

    #############################################
    # Run speedtest (if enabled)
    # (If not enabled, dump adapter info anyway)
    #############################################
    # hold all results in one place
    results_dict = {}

    # define column headers
    column_headers = ['time', 'server_name', 'ping_time', 'download_rate_mbps', 'upload_rate_mbps', 'ssid',
                      'bssid', 'freq_ghz', 'channel', 'phy_rate_mbps', 'signal_level_dbm', 'tx_retries', 'ip_address', 'location']

    results_dict['ssid'] = adapter.get_ssid()
    results_dict['bssid'] = adapter.get_bssid()
    results_dict['freq_ghz'] = adapter.get_freq()
    results_dict['center_freq_ghz'] = adapter.get_center_freq()
    results_dict['channel'] = adapter.get_channel()
    results_dict['channel_width'] = adapter.get_channel_width()
    results_dict['tx_rate_mbps'] = adapter.get_tx_bit_rate()
    results_dict['rx_rate_mbps'] = adapter.get_rx_bit_rate()
    results_dict['tx_mcs'] = adapter.get_tx_mcs()
    results_dict['rx_mcs'] = adapter.get_rx_mcs()
    results_dict['signal_level_dbm'] = adapter.get_signal_level()
    results_dict['tx_retries'] = adapter.get_tx_retries()
    results_dict['ip_address'] = adapter.get_ipaddr()
    results_dict['time'] = int(time.time())
    #results_dict['tags'] = [x.strip() for x in config_vars['tags'].split(',')]
    results_dict['location'] = config_vars['location']

    # test issue flag
    test_issue = False

    # drump out adapter info to log file
    file_logger.info("Wireless connection: SSID:{}, BSSID:{}, Freq:{}, Center Freq:{}, Channel: {}, Channel Width: {}, Tx Phy rate:{}, Rx Phy rate:{}, Tx MCS: {}, Rx MCS: {}, RSSI:{}, Tx retries:{}, IP address:{}".format(results_dict['ssid'],
                                                                                                                                                                                                                             results_dict['bssid'], results_dict['freq_ghz'], results_dict['center_freq_ghz'], results_dict['channel'], results_dict['channel_width'], results_dict[
                                                                                                                                                                                                                                 'tx_rate_mbps'], results_dict['rx_rate_mbps'], results_dict['tx_mcs'], results_dict['rx_mcs'], results_dict['signal_level_dbm'], results_dict['tx_retries'],
                                                                                                                                                                                                                             results_dict['ip_address']))

    # Pre-populate speedtest results vars
    results_dict['ping_time'] = None
    results_dict['download_rate_mbps'] = None
    results_dict['upload_rate_mbps'] = None
    results_dict['server_name'] = None

    file_logger.info("########## speedtest ##########")
    if config_vars['speedtest_enabled'] == 'yes':

        file_logger.info("Starting speedtest...")
        write_status_file("speedtest")

        # check test to Intenet will go via wlan interface
        if check_route_to_dest('8.8.8.8', file_logger) == config_vars['wlan_if']:

            file_logger.info("Speedtest in progress....please wait.")

            # speedtest returns false if there are any issues
            speedtest_results = ooklaspeedtest(
                file_logger, config_vars['server_id'])
            if not speedtest_results == False:

                if DEBUG:
                    print("Main: Speedtest results:")
                    print(speedtest_results)

                # speedtest results
                results_dict['ping_time'] = int(speedtest_results['ping_time'])
                results_dict['download_rate_mbps'] = float(
                    speedtest_results['download_rate'])
                results_dict['upload_rate_mbps'] = float(
                    speedtest_results['upload_rate'])
                results_dict['server_name'] = str(
                    speedtest_results['server_name'])

                file_logger.info("Speedtest ended.")
            else:
                file_logger.error(
                    "Error running speedtest - check logs for info.")
        else:
            file_logger.error(
                "Unable to run Speedtest as route to Internet not via wireless interface.")
            test_issue = True
    else:
        file_logger.info(
            "Speedtest not enabled in config file, just dumping adapter info instead...")

    # dump the results
    data_file = config_vars['speedtest_data_file']
    test_name = "Speedtest"
    send_results(results_dict, column_headers, data_file,
                 test_name, file_logger, DEBUG)

    #############################
    # Run ping test (if enabled)
    #############################
    file_logger.info("########## ping tests ##########")
    if config_vars['ping_enabled'] == 'yes' and test_issue == False:

        file_logger.info("Starting ping test...")
        write_status_file("Ping tests")

        # run ping test
        ping_obj = Pinger(file_logger, platform=platform, debug=DEBUG)

        ping_host1 = config_vars['ping_host1']
        ping_host2 = config_vars['ping_host2']
        ping_host3 = config_vars['ping_host3']
        ping_host4 = config_vars['ping_host4']
        ping_host5 = config_vars['ping_host5']
        ping_hosts = [ping_host1, ping_host2,
                      ping_host3, ping_host4, ping_host5]

        ping_count = config_vars['ping_count']

        # define colum headers for CSV
        column_headers = ['time', 'ping_index', 'ping_host', 'pkts_tx', 'pkts_rx',
                          'percent_loss', 'test_time_ms', 'rtt_min_ms', 'rtt_avg_ms', 'rtt_max_ms', 'rtt_mdev_ms']

        # initial ping to populate arp cache and avoid arp timeput for first test ping
        for ping_host in ping_hosts:
            if ping_host == '':
                continue
            else:
                # check for def_gw keyword
                if ping_host == 'def_gw':
                    ping_host = adapter.get_def_gw()

                # check test to Intenet will go via wlan interface
                if check_route_to_dest(ping_host, file_logger) == config_vars['wlan_if']:
                    ping_obj.ping_host(ping_host, 1)
                else:
                    file_logger.error(
                        "Unable to ping {} as route to destination not over wireless interface...bypassing ping tests".format(ping_host))
                    # we will break here if we have an issue as something bad has happened...don't want to run more tests
                    test_issue = True
                    break

        # run actual ping tests
        ping_index = 0
        delete_file = True
        all_tests_fail = True

        for ping_host in ping_hosts:

            # bail if we have had DNS issues
            if test_issue == True:
                file_logger.error(
                    "As we had previous issues, bypassing ping tests.")
                break

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
                results_dict['time'] = int(time.time())
                results_dict['ping_index'] = ping_index
                results_dict['ping_host'] = ping_result['host']
                results_dict['pkts_tx'] = ping_result['pkts_tx']
                results_dict['pkts_rx'] = ping_result['pkts_rx']
                results_dict['percent_loss'] = ping_result['pkt_loss']
                results_dict['test_time_ms'] = ping_result['test_time']
                results_dict['rtt_min_ms'] = round(
                    float(ping_result['rtt_min']), 2)
                results_dict['rtt_avg_ms'] = round(
                    float(ping_result['rtt_avg']), 2)
                results_dict['rtt_max_ms'] = round(
                    float(ping_result['rtt_max']), 2)
                results_dict['rtt_mdev_ms'] = round(
                    float(ping_result['rtt_mdev']), 2)

                # dump the results
                data_file = config_vars['ping_data_file']
                test_name = "Ping"
                send_results(results_dict, column_headers, data_file, test_name,
                             file_logger, DEBUG, delete_data_file=delete_file)

                file_logger.info("Ping test ended.")

                # Make sure we don't delete data file next time around
                delete_file = False

                if DEBUG:
                    print("Main: Ping test results:")
                    print(ping_result)
                
                # signal that at least one test passed
                all_tests_fail = False

            else:
                file_logger.error("Ping test failed.")
            
        # if all tests fail, and there are more than 2 tests, signal a possible issue
        if all_tests_fail and (ping_index > 1):
            file_logger.error("Looks like quite a few pings failed, incrementing watchdog.")
            inc_watchdog_count()

    else:
        file_logger.info(
            "Ping test not enabled in config file (or previous tests failed), bypassing this test...")

    ###################################
    # Run DNS lookup tests (if enabled)
    ###################################
    file_logger.info("########## dns tests ##########")
    if config_vars['dns_test_enabled'] == 'yes' and test_issue == False:

        file_logger.info("Starting DNS tests...")
        write_status_file("DNS tests")

        dns_targets = [config_vars['dns_target1'], config_vars['dns_target2'],
                       config_vars['dns_target3'], config_vars['dns_target4'], config_vars['dns_target5']]

        dns_index = 0
        delete_file = True

        for dns_target in dns_targets:

            dns_index += 1

            # move on to next if no DNS entry data
            if dns_target == '':
                continue

            dns_obj = DnsTester(file_logger, platform=platform, debug=DEBUG)

            dns_result = dns_obj.dns_single_lookup(dns_target)

            if dns_result:

                column_headers = ['time', 'dns_index',
                                  'dns_target', 'lookup_time_ms']

                # summarise result for log
                result_str = ' {}: {}ms'.format(dns_target, dns_result)

                # drop abbreviated results in log file
                file_logger.info("DNS results: {}".format(result_str))

                results_dict = {
                    'time': int(time.time()),
                    'dns_index': dns_index,
                    'dns_target': dns_target,
                    'lookup_time_ms': dns_result
                }

                # dump the results
                data_file = config_vars['dns_data_file']
                test_name = "DNS"
                send_results(results_dict, column_headers, data_file, test_name,
                             file_logger, DEBUG, delete_data_file=delete_file)

                file_logger.info("DNS test ended.")

                # Make sure we don't delete data file next time around
                delete_file = False

            else:
                file_logger.error(
                    "DNS test error - no results (check logs) - exiting DNS tests")

    else:
        file_logger.info(
            "DNS test not enabled in config file (or previous tests failed), bypassing this test...")

    ###################################
    # Run HTTP lookup tests (if enabled)
    ###################################
    file_logger.info("########## http tests ##########")
    if config_vars['http_test_enabled'] == 'yes' and test_issue == False:

        file_logger.info("Starting HTTP tests...")
        write_status_file("HTTP tests")

        http_targets = [config_vars['http_target1'], config_vars['http_target2'],
                        config_vars['http_target3'], config_vars['http_target4'], config_vars['http_target5']]

        http_index = 0
        delete_file = True
        all_tests_fail = True

        for http_target in http_targets:

            http_index += 1

            # move on to next if no HTTP entry data
            if http_target == '':
                continue

            file_logger.info("Starting http test to : {}".format(http_target))
            http_obj = HttpTester(file_logger, platform=platform, debug=DEBUG)

            http_result = http_obj.http_get(http_target)

            if http_result:

                column_headers = [
                    'time', 'http_index', 'http_target', 'lookup_time_ms', 'http_status_code']

                http_status_code = http_result[0]
                duration = http_result[1]

                # test if http get returned a code - False = bad http get test
                if http_status_code:
                    # summarise result for log
                    result_str = ' {}: {}ms (status code: {})'.format(
                        http_target, duration, http_status_code)

                    # drop abbreviated results in log file
                    file_logger.info("HTTP results: {}".format(result_str))

                    results_dict = {
                        'time': int(time.time()),
                        'http_index': http_index,
                        'http_target': http_target,
                        'lookup_time_ms': duration,
                        'http_status_code': http_status_code
                    }

                    # dump the results
                    data_file = config_vars['http_data_file']
                    test_name = "HTTP"
                    send_results(results_dict, column_headers, data_file, test_name,
                                 file_logger, DEBUG, delete_data_file=delete_file)

                    all_tests_fail = False

                else:
                    file_logger.error(
                        "HTTP test had issue and failed, check agent.log")

                file_logger.info("HTTP test ended.")

                # Make sure we don't delete data file next time around
                delete_file = False

            else:
                file_logger.error(
                    "HTTP test error - no results (check logs) - exiting HTTP tests")
                test_issue = True
                break

        # if all tests fail, and there are more than 2 tests, signal a possible issue
        if all_tests_fail and (http_index > 1):
            file_logger.error("Looks like quite a few http tests failed, incrementing watchdog.")
            inc_watchdog_count()
    else:
        file_logger.info(
            "HTTP test not enabled in config file (or previous tests failed), bypassing this test...")

    ###################################
    # Run iperf3 tcp test (if enabled)
    ###################################
    file_logger.info("########## iperf3 tcp test ##########")
    if config_vars['iperf3_tcp_enabled'] == 'yes' and test_issue == False:

        duration = int(config_vars['iperf3_tcp_duration'])
        port = int(config_vars['iperf3_tcp_port'])
        server_hostname = config_vars['iperf3_tcp_server_hostname']

        file_logger.info("Starting iperf3 tcp test ({}:{})...".format(
            server_hostname, str(port)))
        write_status_file("iperf3 tcp")

        # check test to iperf3 server will go via wlan interface
        if check_route_to_dest(server_hostname, file_logger) == config_vars['wlan_if']:

            # run iperf test
            result = tcp_iperf_client_test(
                file_logger, server_hostname, duration=duration, port=port, debug=False)

            if not result == False:

                results_dict = {}

                column_headers = ['time', 'sent_mbps', 'received_mbps',
                                  'sent_bytes', 'received_bytes', 'retransmits']

                results_dict['time'] = int(time.time())
                results_dict['sent_mbps'] = round(result['sent_mbps'], 1)
                results_dict['received_mbps'] = round(
                    result['received_mbps'], 1)
                results_dict['sent_bytes'] = result['sent_bytes']
                results_dict['received_bytes'] = result['received_bytes']
                results_dict['retransmits'] = result['retransmits']

                # drop abbreviated results in log file
                file_logger.info("Iperf3 tcp results - rx_mbps: {}, tx_mbps: {}, retransmits: {}, sent_bytes: {}, rec_bytes: {}".format(
                    results_dict['received_mbps'], results_dict['sent_mbps'], results_dict['retransmits'], results_dict['sent_bytes'],
                    results_dict['received_bytes']))

                # dump the results
                data_file = config_vars['iperf3_tcp_data_file']
                test_name = "iperf3_tcp"
                send_results(results_dict, column_headers,
                             data_file, test_name, file_logger, DEBUG)

                file_logger.info("Iperf3 tcp test ended.")

            else:
                file_logger.error("Error with iperf3 tcp test, check logs")

        else:
            file_logger.error(
                "Unable to run iperf test to {} as route to destination not over wireless interface...bypassing test".format(server_hostname))
            test_issue = True

    else:
        file_logger.info(
            "Iperf3 tcp test not enabled in config file (or previous tests failed), bypassing this test...")

    ###################################
    # Run iperf3 udp test (if enabled)
    ###################################
    file_logger.info("########## iperf3 udp test ##########")
    if config_vars['iperf3_udp_enabled'] == 'yes' and test_issue == False:

        duration = int(config_vars['iperf3_udp_duration'])
        port = int(config_vars['iperf3_udp_port'])
        server_hostname = config_vars['iperf3_udp_server_hostname']
        bandwidth = int(config_vars['iperf3_udp_bandwidth'])

        file_logger.info("Starting iperf3 udp test ({}:{})...".format(
            server_hostname, str(port)))
        write_status_file("iperf3 udp")

        if check_route_to_dest(server_hostname, file_logger) == config_vars['wlan_if']:

            result = udp_iperf_client_test(
                file_logger, server_hostname, duration=duration, port=port, bandwidth=bandwidth, debug=False)

            if not result == False:

                results_dict = {}

                column_headers = ['time', 'bytes', 'mbps', 'jitter_ms',
                                  'packets', 'lost_packets', 'lost_percent']

                results_dict['time'] = int(time.time())
                results_dict['bytes'] = result['bytes']
                results_dict['mbps'] = round(result['mbps'], 1)
                results_dict['jitter_ms'] = round(result['jitter_ms'], 1)
                results_dict['packets'] = result['packets']
                results_dict['lost_packets'] = result['lost_packets']
                results_dict['lost_percent'] = round(result['lost_percent'], 1)

                # workaround for crazy jitter figures sometimes seen
                if results_dict['jitter_ms'] > 2000:
                    file_logger.error("Received very high jitter value({}), set to none".format(
                        results_dict['jitter_ms']))
                    results_dict['jitter_ms'] = None

                # drop results in log file
                file_logger.info("Iperf3 udp results - mbps: {}, packets: {}, lost_packets: {}, lost_percent: {}, jitter: {}, bytes: {}".format(
                    results_dict['mbps'], results_dict['packets'], results_dict['lost_packets'], results_dict['lost_percent'],
                    results_dict['jitter_ms'], results_dict['bytes']))

                # dump the results
                data_file = config_vars['iperf3_udp_data_file']
                test_name = "iperf_udp"
                send_results(results_dict, column_headers,
                             data_file, test_name, file_logger, DEBUG)

                file_logger.info("Iperf3 udp test ended.")

            else:
                file_logger.error("Error with iperf3 udp test, check logs")

        else:
            file_logger.error(
                "Unable to run iperf test to {} as route to destination not over wireless interface...bypassing test".format(server_hostname))
            test_issue = True

    else:
        file_logger.info(
            "Iperf3 udp test not enabled in config file (or previous tests failed), bypassing this test...")

    #####################################
    # Run DHCP renewal test (if enabled)
    #####################################
    file_logger.info("########## dhcp test ##########")
    if config_vars['dhcp_test_enabled'] == 'yes' and test_issue == False:

        file_logger.info("Starting DHCP renewal test...")
        write_status_file("DHCP renew")

        dhcp_obj = DhcpTester(file_logger, platform=platform, debug=DEBUG)

        renewal_result = dhcp_obj.dhcp_renewal(
            wlan_if, mode=config_vars['dhcp_test_mode'])

        if renewal_result:

            column_headers = ['time', 'renewal_time_ms']

            results_dict = {
                'time': int(time.time()),
                'renewal_time_ms': renewal_result,
            }

            # dump the results
            data_file = config_vars['dhcp_data_file']
            test_name = "DHCP"
            send_results(results_dict, column_headers, data_file,
                         test_name, file_logger, DEBUG)

            file_logger.info("DHCP test ended.")

        else:
            file_logger.error("DHCP test error - no results (check logs)")

    else:
        file_logger.info(
            "DHCP test not enabled in config file (or previous tests failed), bypassing this test...")

    # get rid of log file
    write_status_file("")
    delete_lock_file(lock_file, file_logger)
    file_logger.info("########## end ##########")

    # decrement watchdog as we ran OK
    if test_issue == False:
        dec_watchdog_count()

    # check if we need to reboot (and that it's time to reboot)
    if config_vars['unit_bouncer']:
        check_for_bounce(bounce_file, file_logger)


###############################################################################
# End main
###############################################################################

if __name__ == "__main__":
    main()
