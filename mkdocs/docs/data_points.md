# Data Points Reference Guide

## Background

The wiperf probe collects a variety of data points about various aspects of network connectivity and performance. It then makes those data points available to a number of databases via their standard API (e.g. Splunk, InfluxDB etc.).

The data collected in all instances is the same, but the format of the data presented to each type of database varies depending on the their API and formatting rules and syntax.

This document details the data points collected by the probe. These field names and the data values should be the same no matter which database is used. 

The probe may collect data for the following network tests, depending upon its configuration:

- [Wireless network connectivity details](#wireless-network-connectivity)
- [Speedtest testing results data](#speedtest-results)
- [ICMP ping tests to various destinations](#ping-results)
- [DNS lookup tests to various destinations](#dns-results)]
- [HTTP (web) tests to various destinations](#http-results)
- [iperf3 TCP test to a nominated iperf3 server](#iperf3-tcp-results)
- [iperf3 UDP test to a nominated iperf3 server](#iperf3-udp-results)
- [DHCP renewal test to test DHCP performance on network to which the WLAN Pi is connected](#dhcp-test-results)
- [SMB/CIFS file copy tests from various desinations](#smb-results)
- [Poller Errors](#poller-errors)
- [Poll Status Information](#poll-status-info)

The tests are run each time the wiperf process is triggered (usually every 5 minutes from a local cron job). The tests that are run, together with test configuration parameters are configured in the config.ini file.

Here are the data points that may be collected, displayed by test type:

## Data Points Details


### Wireless Network Connectivity

**(Data source: wiperf-network)**

* time : Unix timestamp of time test was performed
* ssid : The network name of the wireless network to which the wiperf probe is currently connected 
* bssid : The basic service set identifier (i.e. MAC address) of the radio to which the wiperf probe is currently connected
* freq_ghz : The centre frequency of the channel on which the probe is operating (note this may be different to the primary channel centre freq if a bonded channel is in use)
* center_freq_ghz : The centre frequency of the primary channel on which the probe is operating 
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

**(Data source: wiperf-speedtest)**

* time : Unix timestamp of time test was performed
* ping_time : The RTT of a ping test to the speedtest server
* download_rate_mbps : The throughput rate achieved when receiving data from the speedtest server in megabits per second
* upload_rate_mbps : The throughput rate achieved when sending data to the speedtest server in megabits per second
* server_name : The name of the speedtest server used for this test

### Ping Results

**(Data source: wiperf-ping)**

* time : Unix timestamp of time test was performed
* ping_index : wiperf runs up to 5 instances of ping test via its configuration file. This index uniquely identifies each instance.
* ping_host : The IP address or hostname of the target host/site being pinged
* pkts_tx : The number of ping request packets sent during the ping test
* pkts_rx : The number of ping response packets received back during the ping test
* percent_loss : The percentage (%) of packets lost during the test (i.e. how many responses were received compared to requests sent)
* test_time_ms : How long the ping test took in total
* rtt_min_ms : The minimum round trip time of all ping tests to this test instance in milliseconds
* rtt_avg_ms : The average round trip time of all ping tests to this test instance in milliseconds
* rtt_max_ms : The maximum round trip time of all ping tests to this test instance in milliseconds
* rtt_mdev_ms : Standard deviation of all ping tests to this test instance (...no, I don't know either...but you'll look cool at dinner parties if you mention it.)

### DNS Results

**(Data source: wiperf-ping)**

* time : Unix timestamp of time test was performed
* dns_index : wiperf runs up to 5 instances of DNS test via its configuration file. This index uniquely identifies each instance.
* dns_target : The domain name of the target host/site which is the subject of the DNS lookup test
* lookup_time_ms : The time taken to perform the DNS lookup in milliseconds

### HTTP Results

**(Data source: wiperf-http)**

* time : Unix timestamp of time test was performed
* http_index : wiperf runs up to 5 instances of HTTP test via its configuration file. This index uniquely identifies each instance.
* http_target : The domain name (or IP address) of the target site which is the subject of the HTTP test
* http_get_time_ms : The time taken (in mS) to retrieve the html page from the target site in milliseconds
* http_server_response_time_ms: The time taken (in mS) to receive the response headers from the target site. This is a more useful figure in many instances, as it does not include the page load time to is more indicative of the web server RTT.
* http_status_code : The HTTP status code returned from the target site in this test instance (200 is good, other values have varying meanings: https://en.wikipedia.org/wiki/List_of_HTTP_status_codes )

### iperf3 TCP Results

**(Data source: wiperf-iperf3-tcp)**

* time : Unix timestamp of time test was performed
* sent_mbps : The transmit throughput achieved (in megabits per seconds) during the TCP iperf test
* received_mbps : The receive throughput achieved (in megabits per seconds) during the TCP iperf test
* sent_bytes : The number of bytes (i.e. data volume) sent from the probe to the iperf server during the test
* received_bytes : The number of bytes (i.e. data volume) received by the probe from the iperf server during the test
* retransmits : The number of times frames had to be re=transmitted during the test

### iperf3 UDP Results

**(Data source: wiperf-iperf3-udp)**

* time : Unix timestamp of time test was performed
* bytes : The number of bytes transferred from the probe to the iperf server during the test
* mbps : The throughput achieved (in megabits per second) during the iperf test when sending data to the iperf server
* jitter_ms : The level of jitter measured (in milliseconds) during the test
* packets : The number of packets sent from the probe to the iperf server during the test
* lost_packets : The number of transmitted packets lost during the test
* lost_percent : The percentage of transmitted packets lost during the test

### DHCP Test Results

**(Data source: wiperf-dhcp)**

* time : Unix timestamp of time test was performed
* renewal_time_ms : The time taken for the probe to renew it's IP address in milliseconds

### SMB Results

**(Data source: wiperf-smb)**

* time : Unix timestamp of time test was performed
* smb_index: test index number
* smb_host: name/IP of host under test
* filename: name of file being copied during the test
* smb_time: the file transfer time in mS
* smb_rate: the file transfer rate in Mbps

### Poller Errors

**(Data source: wiperf-poll-errors)**

* time : Unix timestamp of time test was performed
* error_message: text string containing error message

### Poll Status Info

**(Data source: wiperf-poll-status)**

* time : Unix timestamp of time test was performed
* network: text string indicating if network connection up OK
* ip: IP address being used by probe network connection
* speedtest: text string indicating if test completed/failed/disabled
* ping: text string indicating if test completed/failed/disabled
* dns: text string indicating if test completed/failed/disabled
* http: text string indicating if test completed/failed/disabled
* iperf_tcp: text string indicating if test completed/failed/disabled
* iperf_udp: text string indicating if test completed/failed/disabled
* dhcp: text string indicating if test completed/failed/disabled
* smb: text string indicating if test completed/failed/disabled
* probe_mode: string indicating if probe in wireless or ethernet mode
* mgt_if: name of management interface (e.g. eth0, wlan0)
* run_time: time is secs that poll cycle took to run




