# Wiperf - config.ini reference guide (work-in-progress)

## Background

The config.ini file controls the operation of the Wiperf utility. It has many options available for maximum flexiblity, but some may need some clarification.

Many options will be fine using the defaults that are supplied with the installed package. However, some will definitely require configuration as they may require values such as IP addresses and port numbers which will vary in each instance where Wiperf is used.

The config.ini file is located in the directory : /home/wlanpi/wiperf

The file is organised in a number of sections that relate to different areas of operation. Each section begins with a name enclosed is square brackets, like this:

```
[Speedtest]
```

Within each section are a number of configurable parameters that are in the format:

```
parameter: value
```

You may also see some lines that begin with a semi-colon. These are comments and have no effect on the operation of Wiperf. You may add, remove or change these as you wish. Here is an example comment:

```
; wlan interface name set this as per the output of an iwconfig command (usually wlan0)
```

We'll take a look at each section of the config file and provide some guidance on suitable parameter values:

- [General Section](#[general]-section)
    - [wlan_if](#wlan_if)
    - [mgt_if](#mgt_if)
    - [platform](#platform)
    - [data_host](#data_host)
    - [data_port](#data-port)
    - [splunk_token](#splunk_token)

## [General] Section

Note: any changes to this section on the WLANPi should only be made when it is running in classic mode (not while in Wiperf mode).

### wlan_if

This parameter contains the name of the WLAN interface on the Pi. This will almost always be 'wlan0', but is provided in case of new use-cases in the future. You can see the WLAN interface name by running the 'ifconfig' command from the CLI of the Pi

Default setting:
```
wlan_if: wlan0
```

### mgt_if

When performance tests have been completed, the results data needs to be sent to a Splunk reporting server. This parameter configures the interface over which this management traffic needs to be sent. 

Getting ths parameter correct for your environment is very important to ensure that test results data makes it back to your Splunk server.

The available options are:

- wlan0 (the first available WLAN port - usually a USB dongle plugged in to the WLANPi)
- eth0 (the internal Ethernet port of the WLANPi)
- zt  (Zerotier (the virtual network service) is installed and used to connect to the Splunk server)

The WANPi is configured to assign a higher cost default route to eth0 by default so that all traffic (tests & test results) will choose the default route provided by wlan0. If eth0 is used as the path to return test results to the Splunk server, then a static route is injected in to the WLANPi route table on start-up to ensure correct routing.

If this parameter is not correctly set, then results data may not make it back to the Splunk server.

Default setting:
```
mgt_if: wlan0
```

### platform

Wiperf is supported on both the WLANPi and Raspberry Pi platforms.  The available options are:

- wlanpi
- rpi

Default setting:
```
platform: wlanpi
```

### data host

This is the hostname or IP address of the Splunk platform where test result data is sent to. If the hostname of the Splunk server is used,it must be resolvable by the WLANPi. 

(Note: If using Zerotier, make sure this is the address of the IP assigned to your Splunk server in the Zerotier dashboard for your network)

Default setting (none):
```
data_host: 
```

### data_port

The network port used to send updates to the Splunk server. By default this is 8088, but this may be changed within the Splunk application if an alternative port is required for your environment

Default setting:
```
data_port: 8088
```

### splunk_token

Splunk will only receive HEC updates from devices that are authorised to send it data. Splunk uses tokens to decide if an update is from a valid device. To view available (or create) tokens within Splunk, view the menu option: "Settings > Data > Data Inputs > HTTP Event Collector"

Here is example token: 84adb9ca-071c-48ad-8aa1-b1903c60310d

Default setting (none):
```
splunk_token: 
```



##########################################################
...edit in progress - nothing below here is complete yet.
##########################################################

; test interval (mins) - how often we want to run the tests (5 is the recommended minimum)
test_interval: 5

; test offset from top of hour (must be less than test interval) - 0 = top of hour, 1 = 1 min after top of hour etc.
test_offset: 0
;
; ------------- Advanced settings for General section, do not change ----------------
; output data format: valid values: csv or json (not required for hec mode)
data_format: json

; data dump location
data_dir: /home/wlanpi/wiperf/data

; Transport methods for data (options: hec, forwarder (Splunk universal forwarder))
data_transport: hec
;------------------------------------------------------------------------------------

; ====================================================================
;  Speedtest test settings
;  (Changes made in this section will be used in next test cycle
;   and may be made while in Wiperf mode on the WLANPi)
; ====================================================================
[Speedtest]
; yes = enabled, no = disabled
enabled: yes
; 
; ------------- Advanced settings for Speedtest section, do not change --------------
; Location of speedtest file for Splunk forwarder to read (do not add file extension)
speedtest_data_file: wiperf-speedtest-splunk
;------------------------------------------------------------------------------------

; ====================================================================
;  Ping tests settings
;  (Changes made in this section will be used in next test cycle
;   and may be made while in Wiperf mode on the WLANPi)
; ====================================================================
[Ping_Test]
; yes = enabled, no = disabled
enabled: yes

; first host we'd like to ping
ping_host1: bbc.co.uk

; first host we'd like to ping
ping_host2: cisco.com

; third host we'd like to ping
ping_host3: google.com

; fourth host we'd like to ping
ping_host4:

; fifth host we'd like to ping
ping_host5:

; number of pings to send
ping_count: 10
;
; ------------ Advanced settings for Ping tests section, do not change --------------
; location of ping test file for Splunk forwarder to read (do not add file extension)
ping_data_file: wiperf-ping-splunk
;------------------------------------------------------------------------------------


; ====================================================================
;  TCP iperf3 tests settings
;  (Changes made in this section will be used in next test cycle
;   and may be made while in Wiperf mode on the WLANPi)
; ====================================================================
[Iperf3_tcp_test]
; yes = enabled, no = disabled
enabled: yes

; IP address of iperf3 server
server_hostname: 192.168.0.14

; iperf server port
port: 5201

; test duration in secs
duration: 20
;
; --------- Advanced settings for TCP iperf3 tests section, do not change -----------
; location of iperf3 tcp file for Splunk forwarder to read (do not add file extension)
iperf3_tcp_data_file: wiperf-iperf3-tcp-splunk
;------------------------------------------------------------------------------------


; ====================================================================
;  UDP iperf3 tests settings
;  (Changes made in this section will be used in next test cycle
;   and may be made while in Wiperf mode on the WLANPi)
; ====================================================================
[Iperf3_udp_test]
; yes = enabled, no = disabled
enabled: yes

; IP address of iperf3 server
server_hostname: 192.168.0.14

; iperf server port
port: 5201

; test duration in secs
duration: 20

; bandwidth in bps
bandwidth: 20000000
;
; --------- Advanced settings for UDP iperf3 tests section, do not change -----------
; location of iperf3 udp file for Splunk forwarder to read (do not add file extension)
iperf3_udp_data_file: wiperf-iperf3-udp-splunk
;------------------------------------------------------------------------------------


; ====================================================================
;  DNS tests settings
;  (Changes made in this section will be used in next test cycle
;   and may be made while in Wiperf mode on the WLANPi)
; ====================================================================
[DNS_test]
; yes = enabled, no = disabled
enabled: yes

; First DNS target
dns_target1: bbc.co.uk

; Second DNS target
dns_target2: cisco.com

; Third DNS target
dns_target3: google.com

; Fourth DNS target
dns_target4:

; Fifth DNS target
dns_target5:
;
; -------------- Advanced settings for DNS tests section, do not change ----------------
; location of DNS results file for Splunk forwarder to read (do not add file extension)
dns_data_file: wiperf-dns-splunk
;---------------------------------------------------------------------------------------

; ====================================================================
;  DHCP tests settings
;  (Changes made in this section will be used in next test cycle
;   and may be made while in Wiperf mode on the WLANPi)
; ====================================================================
[DHCP_test]
; yes = enabled, no = disabled
enabled: yes

; mode: passive or active (active is full release/request but may be disruptve to connectivity - use with caution)
mode: passive
;
; -------------- Advanced settings for DHCP tests section, do not change ---------------
; location of DHCP results file for Splunk forwarder to read (do not add file extension)
dhcp_data_file: wiperf-dhcp-splunk
;---------------------------------------------------------------------------------------