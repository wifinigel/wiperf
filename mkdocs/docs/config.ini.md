# config.ini reference guide  (In development)

## Background

The config.ini file controls the operation of the wiperf utility. It has many options available for maximum flexibility, but some may need some clarification.

Many options will be fine using the defaults that are supplied with the installed package. However, some will definitely require configuration as they may require values such as IP addresses and port numbers which will vary in each instance where wiperf is used.

The config.ini file is located in the directory : /home/wlanpi/wiperf

The file is organised in a number of sections that relate to different areas of operation. Each section begins with a name enclosed is square brackets, like this:

```
[Speedtest]
```

Within each section are a number of configurable parameters that are in the format:

```
parameter: value
```

You may also see some lines that begin with a semi-colon. These are comments and have no effect on the operation of wiperf. You may add, remove or change these as you wish. Here is an example comment:

```
; wlan interface name set this as per the output of an iwconfig command (usually wlan0)
```
## Parameter Reference Guide

We'll take a look at each section of the config file and provide some guidance on suitable parameter values:

- [General Section](#general-section)
    - [wlan_if](#wlan_if)
    - [mgt_if](#mgt_if)
    - [platform](#platform)
    - [exporter_type](#exporter_type)
    - [splunk_host](#splunk_host)
    - [splunk_port](#splunk-port)
    - [splunk_token](#splunk_token)
    - [influx_host](#influx_host)
    - [influx_port](#influx_port)
    - [influx_username](#influx_username)
    - [influx_password](#influx_password)
    - [influx_database](#influx_database)
    - [influx2_host](#influx2_host)
    - [influx2_port](#influx2_port)
    - [influx2_token](#influx2_token)
    - [influx2_bucket](#influx2_bucket)
    - [influx2_org](#influx2_org)
    - [test_interval](#test_interval)
    - [test_offset](#test_offset)
    - [connectivity_lookup](#connectivity_lookup)
    - [location](#location)
    - [data_format](#data_format)
    - [data_dir](#data_dir)
    - [data_transport](#data_transport)
    - [debug](#debug)
    - [cfg_url](#cfg_url) 
    - [cfg_username](#cfg_username) 
    - [cfg_password](#cfg_password) 
    - [cfg_token](#cfg_token) 
    - [cfg_refresh_interval](#cfg_refresh_interval)  
    - [unit_bouncer](#unit_bouncer)
- [Network_Test Section](#network_test-section)
    - [network_data_file](#network_data_file)
- [Speetest Section](#speedtest-section)
    - [enabled](#enabled)
    - [server_id](#server_id)
    - [http_proxy](#http_proxy)
    - [https_proxy](#https_proxy)
    - [no_proxy](#no_proxy)
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
- [HTTP_test Section](#http_test-section)
    - [enabled](#enabled-5)
    - [http_target1](#http_target1)
    - [http_target2](#http_target2)
    - [http_target3](#http_target3)
    - [http_target4](#http_target4)
    - [http_target5](#http_target5)
    - [http_data_file](#http_data_file)
- [DHCP_test Section](#dhcp_test-section)
    - [enabled](#enabled-6)
    - [mode](#mode)
    - [dhcp_data_file](#dhcp_data_file)

## [General] Section

Note: any changes to this section on the WLANPi should only be made when it is running in classic mode (not while in wiperf mode).

### wlan_if

This parameter contains the name of the WLAN interface on the Pi. This will almost always be 'wlan0', but is provided in case of new use-cases in the future. You can see the WLAN interface name by running the 'ifconfig' command from the CLI of the Pi

Default setting:
```
wlan_if: wlan0
```
[top](#parameter-reference-guide)

### mgt_if

When performance tests have been completed, the results data needs to be sent to a reporting server (e.g. Splunk/InfluxDb). This parameter configures the interface over which this management traffic needs to be sent. 

Getting this parameter correct for your environment is very important to ensure that test results data makes it back to your reporting server.

The available options are:

- wlan0 (the first available WLAN port - usually a USB dongle plugged in to the WLANPi)
- eth0 (the internal Ethernet port of the WLANPi)
- zt  (Zerotier (the virtual network service) is installed and used to connect to the reporting server)

The WANPi is configured to assign a higher cost default route to eth0 by default so that all traffic (tests & test results) will choose the default route provided by wlan0. If eth0 is used as the path to return test results to the reporting server, then a static route is injected in to the WLANPi route table on start-up to ensure correct routing.

If this parameter is not correctly set, then results data may not make it back to the reporting server.

Default setting:
```
mgt_if: wlan0
```
[top](#parameter-reference-guide)

### platform (Deprecated)
*(This setting is now deprecated (and unused) - it has been included for historical reference)*

Wiperf is supported on both the WLANPi and Raspberry Pi platforms.  The available options are:

- wlanpi
- rpi

Default setting:
```
platform: wlanpi
```
[top](#parameter-reference-guide)

### exporter_type

Wiperf supports a number of remote data repositories that can be used as targets to store test result data. The available options are:

- splunk
- influxdb
- influxdb2

Default setting:
```
exporter_type: splunk
```
[top](#parameter-reference-guide)

### splunk_host

This is the hostname or IP address of the Splunk platform where test result data is sent to. If the hostname of the Splunk server is used, it must be resolvable by the WLANPi. 

(Note: If using Zerotier, make sure this is the address of the IP assigned to your Splunk server in the Zerotier dashboard for your network)

Default setting (none):
```
splunk_host: 
```
[top](#parameter-reference-guide)

### splunk_port

The network port used to send updates to the Splunk server. By default this is 8088, but this may be changed within the Splunk application if an alternative port is required for your environment

Default setting:
```
splunk_port: 8088
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

### influx_host

This is the hostname or IP address of the Influx (v1.x) platform where test result data is sent to. If the hostname of the Influx server is used, it must be resolvable by the WLANPi. 

(Note: If using Zerotier, make sure this is the address of the IP assigned to your Splunk server in the Zerotier dashboard for your network)

Default setting (none):
```
influx_host: 
```
[top](#parameter-reference-guide)

### influx_port

The network port used to send updates to the Influx (v1.x) server. By default this is 8086, but this may be changed within the Influx application if an alternative port is required for your environment

Default setting:
```
influx_port: 8086
```

[top](#parameter-reference-guide)

### influx_username

The username that will be used to access the Influx (v1.x) server DB to post results data. This username must be configured on the InfluxDB server prior to wiper sending results data to the InfluxDB server.

Default setting (None):
```
influx_username:
```
[top](#parameter-reference-guide)

### influx_password

The password that will be used to access the Influx (v1.x) server DB to post results data. This password must be configured on the InfluxDB server prior to wiper sending results data to the InfluxDB server.

Default setting (None):
```
influx_password:
```
[top](#parameter-reference-guide)

### influx_database

The name of the database on the Influx (v1.x) server DB where wiperf will post results data. This database must have been created on the InfluxDB server prior to wiper sending results data to the InfluxDB server.

Default setting (None):
```
influx_database:
```
[top](#parameter-reference-guide)

### influx2_host

This is the hostname or IP address of the Influx (v2.x) platform where test result data is sent to. If the hostname of the Influx server is used, it must be resolvable by the WLANPi. 

(Note: If using Zerotier, make sure this is the address of the IP assigned to your InfluxDb2 server in the Zerotier dashboard for your network)

Default setting (none):
```
influx2_host: 
```
[top](#parameter-reference-guide)

### influx2_port

The network port used to send updates to the Influx (v2.x) server. By default this is 443 (this assumes the cloud service is used), but this may be changed within the Influx application if an alternative port is required for your environment

Default setting:
```
influx2_port: 443
```

[top](#parameter-reference-guide)

### influx2_token

InfluxDB2 allows the use of authentication tokens when sending results data to the InfluxDB2 server. This provides an easier authentication methods than using a username and password. Once a token has been created on InfluxDB server, it can be used by wiperf to authenticate the results data sent to the InfluxDB2 server

Default setting (none):
```
influx2_token: 
```
[top](#parameter-reference-guide)

### influx2_bucket

Data sent to the InfluxDB2 server from wiperf is stored in a "bucket" in the data store. This field is used to configure the bucket to which wiperf should send it's data.

Default setting (none):
```
influx2_bucket: 
```
[top](#parameter-reference-guide)

### influx2_org

The InfluxDB2 server can be partitioned in to a number of organizations, which contain the buckets where data will be stored. Use this field to configure wiperf to send data to the correct organisation on InfluxDB2.

Default setting (none):
```
influx2_org: 
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

### connectivity_lookup

At the start of each test cycle, a DNS lookup is performed to ensure that DNS is working. By default this is 'google.com' (this was 'bbc.co.uk' on older versions of wiperf). This may be set to any required hostname lookup in instances when the default site may not be available for some reason (e.g. DNS restrictions due to filtering or lack of Internet access)

Default setting:
```
connectivity_lookup: google.com
```
[top](#parameter-reference-guide)

### location

This is a string that can be added to assist with report filtering, if required. Its default value in an empty string. It could be be used in an expression within your reports to filter units based on a location field (for instance)

Default setting:
```
location: 
```
[top](#parameter-reference-guide)

### data_format
(Not currently operational) wiperf has the capability to output data in a number of formats. The current options are: csv or json

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

### debug

To enable enhanced logging in the agent.log file, change this setting to "on"

Default setting:
```
debug: off
```
[top](#parameter-reference-guide)

### cfg_url

If using centralized configuration file retrieval, this field specifies the full URL of the config file on the remote repo. (Note that on GitHub this is the URL of the raw file itself)

If this field is not set, then centralized configuration retrieval is disabled

Default setting (none):
```
cfg_url: 
```
[top](#parameter-reference-guide)

### cfg_username

If username/pasword credentials are used to retrieve the centralized config, this field specifies the usename to be used.

Default setting (none):
```
cfg_username: 
```
[top](#parameter-reference-guide)

### cfg_password

If username/pasword credentials are used to retrieve the centralized config, this field specifies the password to be used.

Default setting (none):
```
cfg_password: 
```
[top](#parameter-reference-guide)

### cfg_token

If a GitHub authentication token is used to retrieve the centralized config, this field specifies the token to be used. (Note: this is used instead of a username/pwd)

Default setting (none):
```
cfg_token: 
```
[top](#parameter-reference-guide)

### cfg_refresh_interval

This field specifies how often (in seconds) the centralized config file should be retrieved . Recommended value: 900 (i.e. 15 mins)

Default setting (none):
```
cfg_refresh_interval: 
```
[top](#parameter-reference-guide)

### unit_bouncer

If you need to bounce (reboot) the unit for some reason on a regular basis, this field can be used to signal to the WLAN Pi each hour at which it must reboot.

The field is a comma separated string that lists the hours at which the unit must reboot (in 24-hour format). The number-format and comma separation are important to get right! Note that the reboot is not exactly on the hour, but will occur at the end of the next test cycle that it is within the hour where a reboot is required. It will only happen once per hour.

Example: the following config will reboot at midnight, 04:00, 08:00, 12:00, 16:00:
```
 unit_bouncer: 00, 06, 12, 18
```
This parameter is commented out by default as it is obviously not something you necessarilly want to switch on accidentally.

Default setting:
```
; unit_bouncer: 00, 06, 12, 18
```
[top](#parameter-reference-guide)

## [Network_Test] Section

### network_data_file

(Advanced setting, do not change) This the file name for modes where data files are dumped locally and also provides the data source for network tests in remote data repositories (e.g. Splunk, InfluxDB) 

Default setting:
```
network_data_file: wiperf-network
```
[top](#parameter-reference-guide)

## [Speedtest] Section

(Changes made in this section will be used in next test cycle and may be made on the fly while in wiperf mode on the WLANPi)

### enabled

Options: yes or no. If set to no, entire section is ignored and no Speedtest is run. When enabled, a speedtest to the Ookla speedtest service is run each test cycle.

Default setting:
```
enabled: yes
```
[top](#parameter-reference-guide)

### server_id

If you wish to specify a particular Ookla speedtest server that the test needs to be run against, you can enter its ID here. This must be the (numeric) server ID of a specific Ookla server taken from : https://c.speedtest.net/speedtest-servers-static.php

**Note this must be the number (NOT url!) taken from the field id="xxxxx".**

If no value is specified, best server is used (default)

Default setting:
```
server_id:
```
[top](#parameter-reference-guide)

### http_proxy
### https_proxy
### no_proxy

If proxy server access is required to run a speedtest, enter the proxy server details here for https & https e.g. 
```
https_proxy: http://10.1.1.1:8080
```

For sites that are not accessed via proxy, use ```no_proxy``` (make sure value enclosed in quotes & comma separated for mutiple values) e.g. 
```
no_proxy: "mail.local, intranet.local"
```

Default settings:
```
http_proxy: 
https_proxy:
no_proxy:
```
[top](#parameter-reference-guide)


### speedtest_data_file

(Advanced setting, do not change) This the file name for modes where data files are dumped locally and also provides the data source for Speedtests in the reporting server (e.g. Splunk/InfluxDB) 

Default setting:
```
speedtest_data_file: wiperf-speedtest
```
[top](#parameter-reference-guide)


## [Ping_Test] Section

(Changes made in this section will be used in next test cycle and may be made on the fly while in wiperf mode on the WLANPi)

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

(Advanced setting, do not change) This the file name for modes where data files are dumped locally and also provides the data source for ping tests in the reporting server (e.g. Splunk.InfuxDB)

Default setting:
```
ping_data_file: wiperf-ping
```
[top](#parameter-reference-guide)

## [Iperf3_tcp_test] Section

(Changes made in this section will be used in next test cycle and may be made on the fly while in wiperf mode on the WLANPi)

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
iperf3_tcp_data_file: wiperf-iperf3-tcp
```
[top](#parameter-reference-guide)

## [Iperf3_udp_test] Section

(Changes made in this section will be used in next test cycle and may be made on the fly while in wiperf mode on the WLANPi)

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
iperf3_udp_data_file: wiperf-iperf3-udp
```
[top](#parameter-reference-guide)

## [DNS_test] Section

(Changes made in this section will be used in next test cycle and may be made on the fly while in wiperf mode on the WLANPi)

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
dns_data_file: wiperf-dns
```
[top](#parameter-reference-guide)

## [HTTP_test] Section

(Changes made in this section will be used in next test cycle and may be made on the fly while in wiperf mode on the WLANPi)

### enabled

Options: yes or no. If set to no, entire section is ignored and no HTTP tests are run. When enabled, HTTP tests are run for each of the ```http_target``` paramters defined in this section. Any targets that have no value entered will be ignored.

Targets must include the full url of each site to be queried (including http:// or https:// element). Valid site address examples:

- http://bbc.co.uk
- https://ebay.com

A http get will be performed for each target and the result code returned.

Default setting:
```
enabled: yes
```
[top](#parameter-reference-guide)

### http_target1

Hostname of first HTTP target. No target details = no test run

Default setting:
```
http_target1: https://ebay.co.uk
```
[top](#parameter-reference-guide)

### http_target2

Hostname of second HTTP target. No target details = no test run

Default setting:
```
http_target2: http://twitter.com
```
[top](#parameter-reference-guide)

### http_target3

Hostname of third HTTP target. No target details = no test run

Default setting:
```
http_target3: https://facebook.com
```
[top](#parameter-reference-guide)

### http_target4

Hostname of fourth HTTP target. No target details = no test run

Default setting:
```
http_target4: https://instagram.com
```
[top](#parameter-reference-guide)

### http_target5

Hostname of fifth HTTP target. No target details = no test run

Default setting: https://amazon.com
```
http_target5: 
```
[top](#parameter-reference-guide)

### http_data_file

(Advanced setting, do not change) This the file name for modes where data files are dumped locally and also provides the data source for HTTP tests in Splunk 

Default setting:
```
http_data_file: wiperf-http
```
[top](#parameter-reference-guide)

## [DHCP_test] Section

(Changes made in this section will be used in next test cycle and may be made on the fly while in wiperf mode on the WLANPi)

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

### mode (deprecated)

__Note:__ This setting has been removed as it caused probe connectivity issues. The probe now only operates in the passive mode. These notes have bene left in for reference for those who used older versions of code or old configuration file. This setting is silently ignored if supplied.

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
dhcp_data_file: wiperf-dhcp
```
[top](#parameter-reference-guide)
