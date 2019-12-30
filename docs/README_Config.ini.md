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
## Paraneter Reference Guide

We'll take a look at each section of the config file and provide some guidance on suitable parameter values:

- [General Section](#general-section)
    - [wlan_if](#wlan_if)
    - [mgt_if](#mgt_if)
    - [platform](#platform)
    - [data_host](#data_host)
    - [data_port](#data-port)
    - [splunk_token](#splunk_token)
    - [test_interval](#test_interval)
    - [test_offset](#test_offset)
    - [data_format](#data_format)
    - [data_dir](#data_dir)
    - [date_transport](#data_transport)
- [Speetest Section](#speedtest-section)

## [General] Section

Note: any changes to this section on the WLANPi should only be made when it is running in classic mode (not while in Wiperf mode).

### wlan_if

This parameter contains the name of the WLAN interface on the Pi. This will almost always be 'wlan0', but is provided in case of new use-cases in the future. You can see the WLAN interface name by running the 'ifconfig' command from the CLI of the Pi

Default setting:
```
wlan_if: wlan0
```
[top](#paraneter-reference-guide)

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
[top](#paraneter-reference-guide)

### platform

Wiperf is supported on both the WLANPi and Raspberry Pi platforms.  The available options are:

- wlanpi
- rpi

Default setting:
```
platform: wlanpi
```
[top](#paraneter-reference-guide)

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

### test_interval

(WLANPi only) This is the interval (in minutes) at which we would like to run the performance tests. The recommened minimum is 5, which is also the default.

(Note: if this setting is too low, scheduled tests may try to run before the previous test sequence has completed, which could cause gaps in your data)

Default setting:
```
test_interval: 5
```

### test_offset

(WLANPi only) By default test run at the interval specified by the ```test_interval``` parameter, which is referenced to the to of the hours (e.g. 5 mins interval will run at 5, 10, 15, 20, 25...etc. mins past the hour). If multiple proes are running, it mau be useful to stagger their start times. By setting ```test_offset``` to a value of one, this will offset all test start times by 1 minutes (i.e. 6,11,16,21,26...etc. mins past the hour)

The default value is zero which means that the default 5,10,15,20... run pattern will be used.

Default setting:
```
test_offset: 0
```

### data_format
(Not currently operational) Wiperf has the capability to output data in a number of formats. The current options are: csv or json

However this field is not currently used, as selecting the 'hec' transport mode (the only supported transport currently) over-rides this field. The value in this filed is currently irrelevant, but it s recommended to leave it at the default setting of ```json```

Default setting:
```
data_format: json
```

### data_dir

This is the directory on the WLANPi/RPi where test result data is dumped. __Do not change this value from the default__. This field is provided for future configuration options if required.

Default setting:
```
data_dir: /home/wlanpi/wiperf/data
```

### data_transport

The currently supported data transport mode is ```hec```. This is the HTTP Event Collector supported natively within the Splunk server. Other transport modes will be suported in the future, but currently this should be left at the default setting of ```hec``.

(Note: the transport method ```forwarder``` is also a valid transport method which provides support for very early versions of this code which used the Splunk Univeral Forwarder. Use of this method is deprecated and will be removed in the near future. Anyone still using the UF should move to using hec ASAP)

Default setting:
```
data_transport: hec
```

## [Speedtest] Section
##########################################################
...edit in progress - nothing below here is complete yet.
##########################################################


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