# Wiperf - Data Points Reference Guide

## Background

The wiperf probe collects a variety of data points about various aspects of network connectivity and performance. It then makes those data points available to a number of databases via their standard API.

The data collected in all instances is the same, but the format of the data presented to each type of database varies depending on the their API and formatting rules and syntax.

This document details the data points collected by the probe. These field names and the data values should be the same no matter which database is used. 

The probe may collect data for the following network tests, depending upon its configuration:

- Wireless network connectivity details
- Speedtest testing results data
- ICMP ping tests to various destinations
- DNS lookup tests to various destinations
- HTTP (web) tests to various destinations
- iperf3 TCP test to a nominated iperf3 server
- iperf3 UDP test to a nominated iperf3 server
- DHCP renewal test to test DHCP performance on network to which the WLAN Pi is connected

The tests are run each time the wiperf process is triggered (usually every 5 minutes from a local cron job). The tests that are run, together with test configuration parameters are configured in the config.ini file.

Here are the data points that may be collected, displayed by test type:

## Data Points Details


### Wireless Network Connectivity



results_dict['ssid'] = self.adapter_obj.get_ssid()
results_dict['bssid'] = self.adapter_obj.get_bssid()
results_dict['freq_ghz'] = self.adapter_obj.get_freq()
results_dict['center_freq_ghz'] = self.adapter_obj.get_center_freq()
results_dict['channel'] = self.adapter_obj.get_channel()
results_dict['channel_width'] = self.adapter_obj.get_channel_width()
results_dict['tx_rate_mbps'] = self.adapter_obj.get_tx_bit_rate()
results_dict['rx_rate_mbps'] = self.adapter_obj.get_rx_bit_rate()
results_dict['tx_mcs'] = self.adapter_obj.get_tx_mcs()
results_dict['rx_mcs'] = self.adapter_obj.get_rx_mcs()
results_dict['signal_level_dbm'] = self.adapter_obj.get_signal_level()
results_dict['tx_retries'] = self.adapter_obj.get_tx_retries()
results_dict['ip_address'] = self.adapter_obj.get_ipaddr()



### Speedtest Results


### Ping Results


### DNS Results


### HTTP Results


### iperf3 TCP Results


### iperf3 UDP Results


### DHCP Test Results





