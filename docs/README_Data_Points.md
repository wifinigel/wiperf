# Wiperf - Data Points Reference Guide

## Background

The wiperf probe collects a variety of data points about various aspects of network connectivity and performance. It then makes those data points available to a number of databases via their standard API (e.g. Splunk, InfluxDB etc.).

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

* time : Unix timestamp of sample time
* ssid : The network name of the wireless network to which the wiperf probe is currently connected 
* bssid : The basic service set identifier (i.e. MAC address) of the radio to which the wiperf probe is currently connected
* freq_ghz : ?
* center_freq_ghz : The centre frequency of the channel on which the probe is operating 
* channel : The channel number on which the probe is operating
* channel_width: The channel width (e.g. 20MHz, 40MHz, 80MHz) of the channel on which the probe is operating
* tx_rate_mbps : The PHY rate at which data is being sent from the probe to the AP (note this is not a throughput rate, just a physical connection rate)
* rx_rate_mbps : The PHY rate at which data is being sent from the AP to the probe (note this is not a throughput rate, just a physical connection rate)
* tx_mcs : For HT & VHT connections, this is the the MCS value used by the probe to the AP
* rx_mcs : For HT & VHT connections, this is the the MCS value used by the AP to the probe
* signal_level_dbm : The power level of the AP radio signal as observed by the probe (in dBm)
* tx_retries : The number of transmitted frames that have had to be sent gain (retried)
* ip_address : The IP address assigned to the probe WLAN NIC

### Speedtest Results

* time : Unix timestamp of sample time
* ping_time : The RTT of a ping test to the speedtest server
* download_rate_mbps : The throughput rate achieved when receiving data from the speedtest server
* upload_rate_mbps : The throughput rate achieved when sending data to the speedtest server
* server_name : The name of the speedtest server used for this test

### Ping Results

* time : Unix timestamp of sample time
* ping_index :
* ping_host :
* pkts_tx :
* pkts_rx :
* percent_loss :
* test_time_ms :
* rtt_min_ms :
* rtt_avg_ms :
* rtt_max_ms :
* rtt_mdev_ms :

### DNS Results

* time : Unix timestamp of sample time
* dns_index : 
* dns_target : 
* lookup_time_ms :

### HTTP Results

* time : Unix timestamp of sample time
* http_index :
* http_target : 
* lookup_time_ms : 
* http_status_code : 

### iperf3 TCP Results

* time : Unix timestamp of sample time
* sent_mbps : 
* received_mbps : 
* sent_bytes : 
* received_bytes : 
* retransmits : 

### iperf3 UDP Results

* time : Unix timestamp of sample time
* bytes : 
* mbps : 
* jitter_ms : 
* packets : 
* lost_packets : 
* lost_percent : 

### DHCP Test Results

* time : Unix timestamp of sample time
* renewal_time_ms : 




