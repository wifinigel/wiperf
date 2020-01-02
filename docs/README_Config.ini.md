# Wiperf - config.ini reference guide

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
## Parameter Reference Guide

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
    - [enabled](#enabled)
    - [speedtest_data_file](#speedtest_data_file)
- [Ping_Test Section](#ping_test-section)
    - [enabled](#enabled-1)
    - [ping_host1](#ping_host1)
    - [ping_host2](#ping_host2)
    - [ping_host3](#ping_host3)
    - [ping_host4](#ping_host4)
    - [ping_host5](#ping_host5)
    - [ping_count](#ping_count)
    - [ping_data_file](#ping_data_file)
- [Iperf3_tcp_test Section](#iperf3_tcp_test-section)
    - [enabled](#enabled-2)
    - [server_hostname](#server_hostname)
    - [port](#port)
    - [duration](#duration)
    - [iperf3_tcp_data_file](#iperf3_tcp_data_file)
- [Iperf3_udp_test Section](#iperf3_udp_test-section)
    - [enabled](#enabled-3)
    - [server_hostname](#server_hostname-1)
    - [port](#port-1)
    - [duration](#duration-1)
    - [bandwidth](#bandwidth)
    - [iperf3_udp_data_file](#iperf3_udp_data_file)
- [DNS_test Section](#dns_test-section)
    - [enabled](#enabled-4)
    - [dns_target1](#dns_target1)
    - [dns_target2](#dns_target2)
    - [dns_target3](#dns_target3)
    - [dns_target4](#dns_target4)
    - [dns_target5](#dns_target5)
    - [dns_data_file](#dns_data_file)
- [DHCP_test Section](#dhcp_test-section)
    - [enabled](#enabled-5)
    - [mode](#mode)
    - [dhcp_data_file](#dhcp_data_file)

## [General] Section

Note: any changes to this section on the WLANPi should only be made when it is running in classic mode (not while in Wiperf mode).

### wlan_if

This parameter contains the name of the WLAN interface on the Pi. This will almost always be 'wlan0', but is provided in case of new use-cases in the future. You can see the WLAN interface name by running the 'ifconfig' command from the CLI of the Pi

Default setting:
```
wlan_if: wlan0
```
[top](#parameter-reference-guide)

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
[top](#parameter-reference-guide)

### platform

Wiperf is supported on both the WLANPi and Raspberry Pi platforms.  The available options are:

- wlanpi
- rpi

Default setting:
```
platform: wlanpi
```
[top](#parameter-reference-guide)

### data host

This is the hostname or IP address of the Splunk platform where test result data is sent to. If the hostname of the Splunk server is used,it must be resolvable by the WLANPi. 

(Note: If using Zerotier, make sure this is the address of the IP assigned to your Splunk server in the Zerotier dashboard for your network)

Default setting (none):
```
data_host: 
```
[top](#parameter-reference-guide)

### data_port

The network port used to send updates to the Splunk server. By default this is 8088, but this may be changed within the Splunk application if an alternative port is required for your environment

Default setting:
```
data_port: 8088
```
[top](#parameter-reference-guide)

### splunk_token

Splunk will only receive HEC updates from devices that are authorised to send it data. Splunk uses tokens to decide if an update is from a valid device. To view available (or create) tokens within Splunk, view the menu option: "Settings > Data > Data Inputs > HTTP Event Collector"

Here is example token: 84adb9ca-071c-48ad-8aa1-b1903c60310d

Default setting (none):
```
splunk_token: 
```
[top](#parameter-reference-guide)

### test_interval

(WLANPi only) This is the interval (in minutes) at which we would like to run the performance tests. The recommened minimum is 5, which is also the default.

(Note: if this setting is too low, scheduled tests may try to run before the previous test sequence has completed, which could cause gaps in your data)

Default setting:
```
test_interval: 5
```
[top](#parameter-reference-guide)

### test_offset

(WLANPi only) By default test run at the interval specified by the ```test_interval``` parameter, which is referenced to the to of the hours (e.g. 5 mins interval will run at 5, 10, 15, 20, 25...etc. mins past the hour). If multiple proes are running, it mau be useful to stagger their start times. By setting ```test_offset``` to a value of one, this will offset all test start times by 1 minutes (i.e. 6,11,16,21,26...etc. mins past the hour)

The default value is zero which means that the default 5,10,15,20... run pattern will be used.

Default setting:
```
test_offset: 0
```
[top](#parameter-reference-guide)

### data_format
(Not currently operational) Wiperf has the capability to output data in a number of formats. The current options are: csv or json

However this field is not currently used, as selecting the 'hec' transport mode (the only supported transport currently) over-rides this field. The value in this filed is currently irrelevant, but it s recommended to leave it at the default setting of ```json```

Default setting:
```
data_format: json
```
[top](#parameter-reference-guide)

### data_dir

This is the directory on the WLANPi/RPi where test result data is dumped. __Do not change this value from the default__. This field is provided for future configuration options if required.

Default setting:
```
data_dir: /home/wlanpi/wiperf/data
```
[top](#parameter-reference-guide)

### data_transport

The currently supported data transport mode is ```hec```. This is the HTTP Event Collector supported natively within the Splunk server. Other transport modes will be suported in the future, but currently this should be left at the default setting of ```hec``.

(Note: the transport method ```forwarder``` is also a valid transport method which provides support for very early versions of this code which used the Splunk Univeral Forwarder. Use of this method is deprecated and will be removed in the near future. Anyone still using the UF should move to using hec ASAP)

Default setting:
```
data_transport: hec
```
[top](#parameter-reference-guide)

## [Speedtest] Section

(Changes made in this section will be used in next test cycle and may be made on the fly while in Wiperf mode on the WLANPi)

### enabled

Options: yes or no. If set to no, entire section is ignored and no Speedtest is run. When enabled, a speedtest to the Ookla speedtest service is run each test cycle.

Default setting:
```
enabled: yes
```
[top](#parameter-reference-guide)

### speedtest_data_file

(Advanced setting, do not change) This the file name for modes where data files are dumped locally and also provides the data source for Speedtests in Splunk 

Default setting:
```
speedtest_data_file: wiperf-speedtest-splunk
```
[top](#parameter-reference-guide)

## [Ping_Test] Section

(Changes made in this section will be used in next test cycle and may be made on the fly while in Wiperf mode on the WLANPi)

### enabled

Options: yes or no. If set to no, entire section is ignored and no ping tests are run. When enabled, up to 5 entries will be targetted with an ICMP ping and the RRT times recorded

Default setting:
```
enabled: yes
```
[top](#parameter-reference-guide)

### ping_host1

IP address or hostname of first ping target. No target details = no test run

Default setting:
```
ping_host1: bbc.co.uk
```
[top](#parameter-reference-guide)

### ping_host2

IP address or hostname of second ping target. No target details = no test run

Default setting:
```
ping_host2: cisco.com
```
[top](#parameter-reference-guide)

### ping_host3

IP address or hostname of third ping target. No target details = no test run

Default setting:
```
ping_host3: google.com
```
[top](#parameter-reference-guide)

### ping_host4

IP address or hostname of fourth ping target. No target details = no test run

Default setting:
```
ping_host4:
```
[top](#parameter-reference-guide)

### ping_host5

IP address or hostname of fifth ping target. No target details = no test run

Default setting:
```
ping_host2: 
```
[top](#parameter-reference-guide)

### ping_count

The number of pings to send for each ping target

Default setting:
```
ping_count: 10
```
[top](#parameter-reference-guide)

### ping_data_file

(Advanced setting, do not change) This the file name for modes where data files are dumped locally and also provides the data source for ping tests in Splunk 

Default setting:
```
ping_data_file: wiperf-ping-splunk
```
[top](#parameter-reference-guide)

## [Iperf3_tcp_test] Section

(Changes made in this section will be used in next test cycle and may be made on the fly while in Wiperf mode on the WLANPi)

### enabled

Options: yes or no. If set to no, entire section is ignored and no tcp iperf3 test is run. When enabled, a tcp iperf3 test will be run to the iperf3 server defined in ```server_hostname``` to the ```port``` network port for the ```duration``` period (in secs) 

Default setting:
```
enabled: yes
```
[top](#parameter-reference-guide)

### server_hostname

The IP address or (resolvable) name of the server running the iperf3 service.

Default setting:
```
server_hostname: 192.168.0.14
```
[top](#parameter-reference-guide)

### port

The network port on the server running iperf3 where the iperf3 service is available (5201 by default).

Default setting:
```
port: 5201
```
[top](#parameter-reference-guide)

### duration

The duration (in seconds) that the iperf3 test will be run for

Default setting:
```
duration: 20
```
[top](#parameter-reference-guide)

### iperf3_tcp_data_file

(Advanced setting, do not change) This the file name for modes where data files are dumped locally and also provides the data source for tcp iperf3 tests in Splunk 

Default setting:
```
iperf3_tcp_data_file: wiperf-iperf3-tcp-splunk
```
[top](#parameter-reference-guide)

## [Iperf3_udp_test] Section

(Changes made in this section will be used in next test cycle and may be made on the fly while in Wiperf mode on the WLANPi)

### enabled

Options: yes or no. If set to no, entire section is ignored and no udp iperf3 test is run. When enabled, a udp iperf3 test will be run to the iperf3 server defined in ```server_hostname``` to the ```port``` network port for the ```duration``` period (in secs), attempting to achieve a data transfer rate of ```bandwidth``` bps. 

Default setting:
```
enabled: yes
```
[top](#parameter-reference-guide)

### server_hostname

The IP address or (resolvable) name of the server running the iperf3 service.

Default setting:
```
server_hostname: 192.168.0.14
```
[top](#parameter-reference-guide)

### port

The network port on the server running iperf3 where the iperf3 service is available (5201 by default).

Default setting:
```
port: 5201
```
[top](#parameter-reference-guide)

### duration

The duration (in seconds) that the iperf3 test will be run for

Default setting:
```
duration: 20
```
[top](#parameter-reference-guide)

### bandwidth

The data rate that will be attempted for the UDP iperf3 test in bps

Default setting:
```
bandwidth: 20000000
```
[top](#parameter-reference-guide)

### iperf3_udp_data_file

(Advanced setting, do not change) This the file name for modes where data files are dumped locally and also provides the data source for udp iperf3 tests in Splunk 

Default setting:
```
iperf3_udp_data_file: wiperf-iperf3-udp-splunk
```
[top](#parameter-reference-guide)

## [DNS_test] Section

(Changes made in this section will be used in next test cycle and may be made on the fly while in Wiperf mode on the WLANPi)

### enabled

Options: yes or no. If set to no, entire section is ignored and no DNS tests are run. When enabled, DNS tests are run for each of the ```dns_target``` paramters defined in this section. Any targets that have no value entered will be ignored.

Default setting:
```
enabled: yes
```
[top](#parameter-reference-guide)

### dns_target1

Hostname of first DNS target. No target details = no test run

Default setting:
```
dns_target1: bbc.co.uk
```
[top](#parameter-reference-guide)

### dns_target2

Hostname of second DNS target. No target details = no test run

Default setting:
```
dns_target2: cisco.com
```
[top](#parameter-reference-guide)

### dns_target3

Hostname of third DNS target. No target details = no test run

Default setting:
```
dns_target3: google.com
```
[top](#parameter-reference-guide)

### dns_target4

Hostname of fourth DNS target. No target details = no test run

Default setting:
```
dns_target4: 
```
[top](#parameter-reference-guide)

### dns_target5

Hostname of fifth DNS target. No target details = no test run

Default setting:
```
dns_target5: 
```
[top](#parameter-reference-guide)

### dns_data_file

(Advanced setting, do not change) This the file name for modes where data files are dumped locally and also provides the data source for DNS tests in Splunk 

Default setting:
```
dns_data_file: wiperf-dns-splunk
```
[top](#parameter-reference-guide)

## [DHCP_test] Section

(Changes made in this section will be used in next test cycle and may be made on the fly while in Wiperf mode on the WLANPi)

### enabled

Options: yes or no. If set to no, entire section is ignored and no DHCP test is run.  Note that the DHCP test has 2 modes :

- passive: only a renewal request is sent (no release of IP)
- active: a release and renew request is performed.

Note that the active setting has shown varying degrees of usefulness in esting. In some scenarios (e.g. when connected via ZeroTier), it has caused connectivity issues, hence the passive setting is a better choice. Obviously, the passive setting does not perform such a rigorous DHCP test and is completed much quicker than the active mode. However, it still provides a useful comparative measure of the reponsivemess of DHCP servers.

Default setting:
```
enabled: yes
```
[top](#parameter-reference-guide)

### mode

Available options:

- passive
- active

The active settings performs a full release/request and may be disruptve to connectivity - use with caution. The passive setting is the recommended option for most situations.


Default setting:
```
mode: passive
```
[top](#parameter-reference-guide)

### dhcp_data_file

(Advanced setting, do not change) This the file name for modes where data files are dumped locally and also provides the data source for DHCP tests in Splunk 

Default setting:
```
dhcp_data_file: wiperf-dhcp-splunk
```
[top](#parameter-reference-guide)
