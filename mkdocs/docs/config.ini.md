Title: config.ini Reference Guide
Authors: Nigel Bowden

# config.ini Reference Guide

## Background

The config.ini file controls the operation of the wiperf utility. It has many options available for maximum flexibility, but some may need some clarification.

Many options will be fine using the defaults that are supplied with the installed package. However, some will definitely require configuration as they may require values such as IP addresses and port numbers which will vary in each instance where wiperf is used.

The config.ini file is located in the directory : /etc/wiperf

Note that an initial sample configuration file is supplied which is named: `config.default.ini`. This file should be copied to `config.ini` and this new file customised with the settings required for your environment. (Note: the `config.default.ini` file is not used by wiperf)

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
    - [probe_mode](#probe_mode)
    - [eth_if](#eth_if)
    - [wlan_if](#wlan_if)
    - [mgt_if](#mgt_if)
    - [platform](#platform)
    - [exporter_type](#exporter_type)
    - [results_spool_enabled](#results_spool_enabled)
    - [results_spool_max_age](#results_spool_max_age)
    - [error_messages_enabled](#error_messages_enabled)
    - [error_messages_limit](#error_messages_limit)
    - [poller_reporting_enabled](#poller_reporting_enabled)
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
    - [cache_enabled](#cache_enabled)
    - [cache_data_format](#cache_data_format)
    - [cache_retention_period](#cache_retention_period)
    - [cache_filter](#cache_filter)
    - [test_interval](#test_interval)
    - [test_offset](#test_offset)
    - [connectivity_lookup](#connectivity_lookup)
    - [location](#location)
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
    - [provider](#provider)
    - [server_id](#server_id)
    - [librespeed_args](#librespeed_args)
    - [http_proxy](#http_proxy)
    - [https_proxy](#https_proxy)
    - [no_proxy](#no_proxy)
    - [speedtest_data_file](#speedtest_data_file)
- [Ping_Test Section](#ping_test-section)
    - [enabled](#enabled-1)
    - [ping_targets_count](#ping_targets_count)
    - [ping_host1](#ping_host1)
    - [ping_host2](#ping_host2)
    - [ping_hostN](#ping_hostN)
    - [ping_count](#ping_count)
    - [ping_timeout](#ping_timeout)
    - [ping_interval](#ping_interval)
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
    - [dns_targets_count](#dns_targets_count)
    - [dns_target1](#dns_target1)
    - [dns_target2](#dns_target2)
    - [dns_targetN](#dns_target3)
    - [dns_data_file](#dns_data_file)
- [HTTP_test Section](#http_test-section)
    - [enabled](#enabled-5)
    - [http_targets_count](#http_targets_count)
    - [http_target1](#http_target1)
    - [http_target2](#http_target2)
    - [http_targetN](#http_targetN)
    - [http_data_file](#http_data_file)
- [DHCP_test Section](#dhcp_test-section)
    - [enabled](#enabled-6)
    - [mode](#mode)
    - [dhcp_data_file](#dhcp_data_file)
- [SMB_test Section](#smb_test-section)
    - [enabled](#enabled-7)
    - [smb_targets_count](#smb_targets_count)
    - [smb_global_username](#smb_global_username)
    - [smb_global_password](#smb_global_password)
    - [smb_hostN](#smb_hostN)
    - [smb_usernameN](#smb_usernameN) 
    - [smb_passwordN](#smb_passwordN) 
    - [smb_pathN](#smb_pathN)
    - [smb_filenameN](#smb_filenameN) 
    - [smb_data_file](#smb_data_file)

## [General] Section

Note: any changes to this section on the WLAN Pi should only be made when it is running in classic mode (not while in wiperf mode).

### probe_mode

The probe may be run in one of two modes:

- wireless
- ethernet

In 'wireless' mode, all tests are run over the Wi-Fi NIC interface to test wireless connectivity & performance. In 'ethernet' mode, all tests are performed over the wired, ethernet interface.

Default setting:
```
probe_mode: wireless
```
[top](#parameter-reference-guide)

### eth_if

This parameter contains the name of the ethernet interface on the probe. This will almost always be 'eth0', but is provided in case of new use-cases in the future. You can see the Ethernet interface name by running the 'ifconfig' command from the CLI of the probe.

Default setting:
```
eth_if: eth0
```
[top](#parameter-reference-guide)

### wlan_if

This parameter contains the name of the WLAN interface on the probe. This will almost always be 'wlan0', but is provided in case of new use-cases in the future. You can see the WLAN interface name by running the 'ifconfig' command from the CLI of the probe.

Default setting:
```
wlan_if: wlan0
```
[top](#parameter-reference-guide)

### mgt_if

When performance tests have been completed, the results data needs to be sent to a reporting server (e.g. Splunk/InfluxDb). This parameter configures the interface over which this management traffic needs to be sent. 

Getting this parameter correct for your environment is very important to ensure that test results data makes it back to your reporting server.

The available options are:

- wlan0 (the first available WLAN port - usually a USB dongle plugged in to the WLAN Pi, or the internal wireless NIC on the RPi)
- eth0 (the internal Ethernet port of the probe)
- ztxxxxxxxx  (Zerotier (the virtual network service) is installed and used to connect to the reporting server - note that the 'xxxxxxx' string needs to be replaced with the actual detail of your Zerotier interface, which will vary on each probe)
- lo (Local loopback interface 0 - this may be used on an RPi when running Influx and Grafana on the probe...yes, it can be done, but this isn't the intended way of running wiperf...your mileage may vary.)

The WLANPi is configured to assign a higher cost default route to eth0 by default so that all traffic (tests & test results) will choose the default route provided by wlan0. If eth0 is used as the path to return test results to the reporting server, then a static route is injected in to the probe route table on start-up to ensure correct routing.

If this parameter is not correctly set, then results data may not make it back to the reporting server.

Default setting:
```
mgt_if: wlan0
```
[top](#parameter-reference-guide)

### platform (Deprecated)
*(This setting is now deprecated (and unused) - it has been included for historical reference)*

Wiperf is supported on both the WLAN Pi and Raspberry Pi platforms.  The available options are:

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

### results_spool_enabled

!!! Note
    New for V2.1

If the mgt platform becomes unavailable, results may be spooled to a local directory for later upload when connectivity is restored.This is enabled by default, but may be disabled for purposes of management traffic bandwidth reduction if required.

Data files are spooled in to the directory: `/etc/spool/wiperf`.

Options: yes or no. If set to no, no results are save for later transmission to the management server.

Default setting:
```
results_spool_enabled: yes
```
[top](#parameter-reference-guide)

### results_spool_max_age

!!! Note
    New for V2.1

If results spooling is enabled, it may be desirable to set the duration for which files are retained (e.g. to avoid running out of storage space). This parameter defines the amount of time (in minutes) that data files are retained.

By default, this parameter is set to 60 minutes. This means that if communication to the management server is lost for more than 60 minutes, locally stored data files older than 60 minutes are deleted.

Default setting:
```
results_spool_max_age: 60
```
[top](#parameter-reference-guide)

### error_messages_enabled

!!! Note
    New for V2.1

Errors experienced by the poller are reported back as data to the management platform by default. This allows visibility of failing tests and may provide useful diagnostics information.

If this data is not required (e.g. to preserve bandwitdh), then the export of these message to the management server may be disabled.

Options: yes or no. If set to no, no poller error data is exported to the management platform.

Default setting:
```
error_messages_enabled: yes
```
[top](#parameter-reference-guide)

### error_messages_limit

!!! Note
    New for V2.1

To prevent overwhelming the management platform with error messages, this parameter set the maximum number of error messages which may be exported per poll cycle.

Default setting:
```
error_messages_limit: 5
```
[top](#parameter-reference-guide)

### poller_reporting_enabled

!!! Note
    New for V2.1

At the end of each poll cycle, a summary of which tests passed/failed may be returned to allow reporting. This may be disabled for purposes of management traffic bandwidth reduction, if required.

Options: yes or no. If set to no, no summary data is exported to the management platform.

Default setting:
```
poller_reporting_enabled: yes
```
[top](#parameter-reference-guide)

### splunk_host

This is the hostname or IP address (ipv4 or ipv6) of the Splunk platform where test result data is sent to. If the hostname of the Splunk server is used, it must be resolvable by the probe. 

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

This is the hostname or IP address (ipv4 or ipv6) of the Influx (v1.x) platform where test result data is sent to. If the hostname of the Influx server is used, it must be resolvable by the probe. 

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

This is the hostname or IP address of the Influx (v2.x) platform where test result data is sent to. If the hostname of the Influx server is used, it must be resolvable by the probe. 

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

### cache_enabled

!!! Note
    New for V2.1

Results data may be cached in the local file system of the probe for later inspection or retrieval by user defined methods. By default, files are stored in local probe directory: /var/cache/wiperf.

Note: This mechanism is different to the spooling feature which is purely for store and forward of data during breaks in comms to the management platform. 

Options: yes or no. If set to no, no test data is cached on the local probe file system

Default setting:
```
cache_enabled: no 
```
[top](#parameter-reference-guide)

### cache_data_format

!!! Note
    New for V2.1

If data caching is enabled, it may be stored in CSV of JSON format.

Options: csv or json

Default setting:
```
cache_data_format: csv 
```
[top](#parameter-reference-guide)

### cache_retention_period

!!! Note
    New for V2.1

This is the number of days of data that will be retained local cache files before being deleted. This is to conserve local storage space.

Default setting:
```
cache_retention_period: 3
```
[top](#parameter-reference-guide)

### cache_filter

!!! Note
    New for V2.1

This provides a data source filter so that only specific data sources are locally cached (e.g. to cache only http & ping data, specify: `wiperf-http, wiperf-ping`)

Default setting (none):
```
cache_filter:
```
[top](#parameter-reference-guide)

### test_interval

(WLAN Pi only) This is the interval (in minutes) at which we would like to run the performance tests. The recommened minimum is 5, which is also the default.

(Note: if this setting is too low, scheduled tests may try to run before the previous test sequence has completed, which could cause gaps in your data)

Default setting:
```
test_interval: 5
```
[top](#parameter-reference-guide)

### test_offset

(WLAN Pi only) By default test run at the interval specified by the ```test_interval``` parameter, which is referenced to the to of the hours (e.g. 5 mins interval will run at 5, 10, 15, 20, 25...etc. mins past the hour). If multiple proes are running, it mau be useful to stagger their start times. By setting ```test_offset``` to a value of one, this will offset all test start times by 1 minutes (i.e. 6,11,16,21,26...etc. mins past the hour)

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
(Note: using an access token is a MUCH better idea...see below)

Default setting (none):
```
cfg_username: 
```
[top](#parameter-reference-guide)

### cfg_password

If username/pasword credentials are used to retrieve the centralized config, this field specifies the password to be used.
(Note: using an access token is a MUCH better idea...see below)

Default setting (none):
```
cfg_password: 
```
[top](#parameter-reference-guide)

### cfg_token

If a GitHub authentication token is used to retrieve the centralized config, this field specifies the token to be used. (Note: this is used instead of a username/pwd)

Check out this page to find out more about creating access tokens: [https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token)

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

### debug

To enable enhanced logging in the agent.log file, change this setting to "on"

Default setting:
```
debug: off
```
[top](#parameter-reference-guide)

### unit_bouncer

If you need to bounce (reboot) the unit for some reason on a regular basis, this field can be used to signal to the WLAN Pi each hour at which it must reboot.

The field is a comma separated string that lists the hours at which the unit must reboot (in 24-hour format). The number-format and comma separation are important to get right! Note that the reboot is not exactly on the hour, but will occur at the end of the next test cycle that it is within the hour where a reboot is required. It will only happen once per hour.

Example: the following config will reboot at midnight, 04:00, 08:00, 12:00, 16:00:
```
 unit_bouncer: 00, 06, 12, 18
```
This parameter is commented out by default as it is obviously not something you necessarily want to switch on accidentally.

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

(Changes made in this section will be used in next test cycle and may be made on the fly while in wiperf mode on the WLAN Pi)

### enabled

Options: yes or no. If set to no, entire section is ignored and no Speedtest is run. When enabled, a speedtest to the speedtest service is run each test cycle.

Default setting:
```
enabled: yes
```
[top](#parameter-reference-guide)

### provider

!!! Note
    New for V2.1

Starting in version 2.1 a choice of speedtest provider is available. Tests may be run against the Ookla or Librespeed speedtest services

Options: ookla or librespeed

(__Note__: ensure that the Librespeed client is installed on your probe if using the librespeed option - it is not installed as part of the probe package - see wiperf.net for more details)

Default setting:
```
provider: ookla
```
[top](#parameter-reference-guide)

### server_id

!!! Note
    Updated for V2.1

If you wish to specify a particular Ookla speedtest server that the test needs to be run against, you can enter its ID here. This must be the (numeric) server ID of a specific Ookla server taken from : https://c.speedtest.net/speedtest-servers-static.php

**Note this must be the number (NOT url!) taken from the field id="xxxxx".**

If you wish to specify a Librespeed server, enter the numeric server ID of the server listed in the available servers seen by running the Librespeed CLI command: `librespeed-cli --list`

If no value is specified, best server is used (default) - __Note__: testing has shown that some versions of the Librespeed client will not successfully choose a best server - specify a server ID if you are having issues with the test not running as expected.

Default setting:
```
server_id:
```
[top](#parameter-reference-guide)

### librespeed_args

!!! Note
    New for V2.1

If you wish to pass additional args to pass to Librespeed CLI command, then add them to this configuration parameter (e.g. --local-json /etc/wipef/localserver.json --duration 20) - __Note: Librespeed only__

Default setting (no value):
```
librespeed_args:
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

Default settings (no value):
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

(Changes made in this section will be used in next test cycle and may be made on the fly while in wiperf mode on the WLAN Pi)

### enabled

Options: yes or no. If set to no, entire section is ignored and no ping tests are run. When enabled, up to 5 entries will be targetted with an ICMP ping and the RRT times recorded

Default setting:
```
enabled: yes
```
[top](#parameter-reference-guide)

### ping_targets_count

!!! Note
    New for V2.2

The number of targets hosts/addresses that will be pinged. There should be a corresponding number of `ping_host` entries for this value

Default setting:
```
ping_targets_count: 2
```
[top](#parameter-reference-guide)

### ping_host1

IP address or hostname of first ping target. No target details = no test run

Default setting:
```
ping_host1: google.com
```
[top](#parameter-reference-guide)

### ping_host2

IP address or hostname of second ping target. No target details = no test run

Default setting:
```
ping_host2: cisco.com
```
[top](#parameter-reference-guide)

### ping_hostN

IP address or hostname of "Nth" ping target. No target details = no test run.

As many of these entries as are required may be added (must match number of entries specified in `ping_targets_count` field).

Default setting:
```
ping_hostN: 
```
[top](#parameter-reference-guide)

### ping_count

The number of pings to send for each ping target

Default setting:
```
ping_count: 10
```
[top](#parameter-reference-guide)

### ping_timeout

!!! Note
    New for V2.2

The timeout in seconds that is used for each ping test.

Default setting:
```
ping_count: 1
```
[top](#parameter-reference-guide)

### ping_interval

!!! Note
    New for V2.2

The timeout in seconds that is used between each ping test

Default setting:
```
ping_count: 0.2
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

(Changes made in this section will be used in next test cycle and may be made on the fly while in wiperf mode on the WLAN Pi)

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
server_hostname: 
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
duration: 10
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

(Changes made in this section will be used in next test cycle and may be made on the fly while in wiperf mode on the WLAN Pi)

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
server_hostname: 
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
duration: 10
```
[top](#parameter-reference-guide)

### bandwidth

The data rate that will be attempted for the UDP iperf3 test in bps

Default setting:
```
bandwidth: 2000000
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

(Changes made in this section will be used in next test cycle and may be made on the fly while in wiperf mode on the WLAN Pi)

### enabled

Options: yes or no. If set to no, entire section is ignored and no DNS tests are run. When enabled, DNS tests are run for each of the ```dns_target``` paramters defined in this section. Any targets that have no value entered will be ignored.

Default setting:
```
enabled: yes
```
[top](#parameter-reference-guide)

### dns_targets_count

!!! Note
    New for V2.2

The number of targets hosts that will be tested. There should be a corresponding number of `dns_target` entries for this value

Default setting:
```
dns_targets_count: 2
```
[top](#parameter-reference-guide)

### dns_target1

Hostname of first DNS target. No target details = no test run

Default setting:
```
dns_target1: google.com
```
[top](#parameter-reference-guide)

### dns_target2

Hostname of second DNS target. No target details = no test run

Default setting:
```
dns_target2: cisco.com
```
[top](#parameter-reference-guide)

### dns_targetN

Hostname of "Nth" DNS target. No target details = no test run

As many of these entries as are required may be added (must match number of entries specified in `dns_targets_count` field).

Default setting:
```
dns_targetN: 
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

(Changes made in this section will be used in next test cycle and may be made on the fly while in wiperf mode on the WLAN Pi)

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

### http_targets_count

!!! Note
    New for V2.2

The number of targets hosts that will be tested. There should be a corresponding number of `http_target` entries for this value

Default setting:
```
http_targets_count: 2
```
[top](#parameter-reference-guide)

### http_target1

Hostname of first HTTP target. No target details = no test run

Default setting:
```
http_target1: https://google.com
```
[top](#parameter-reference-guide)

### http_target2

Hostname of second HTTP target. No target details = no test run

Default setting:
```
http_target2: https://cisco.com
```
[top](#parameter-reference-guide)

### http_targetN

Hostname of "Nth" HTTP target. No target details = no test run

As many of these entries as are required may be added (must match number of entries specified in `http_targets_count` field).

Default setting:
```
http_targetN: 
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

(Changes made in this section will be used in next test cycle and may be made on the fly while in wiperf mode on the WLAN Pi)

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

## [SMB_test] Section

(Changes made in this section will be used in next test cycle and may be made on the fly while in wiperf mode on the WLAN Pi)

### enabled

!!! Note
    New for V2.1

Options: yes or no. If set to no, entire section is ignored and no SMB tests are run.  Note that the DHCP test has 2 modes :

Default setting:
```
enabled: no
```
[top](#parameter-reference-guide)

### smb_targets_count

!!! Note
    New for V2.2

The number of SMB target hosts that will be tested. There should be a corresponding number of SMB host target entries for this value

Default setting:
```
smb_targets_count: 2
```
[top](#parameter-reference-guide)

### smb_global_username
### smb_global_password

!!! Note
    New for V2.1

These are the username and password credentials to be used for all SMB tests where a test-specific username/password has not been provided.

Default setting (no value):
```
smb_global_username: 
smb_global_passwrod:
```
[top](#parameter-reference-guide)

### smb_hostN

!!! Note
    New for V2.1

The hostname or IP address to be used for SMB test number 'N' (1-N)

Default setting:
```
smb_hostN: 
```
[top](#parameter-reference-guide)

### smb_usernameN
### smb_passwordN 

!!! Note
    New for V2.1

The username & password to be used for SMB test number 'N' (1-N). Note the global username/password credential is use if a per-test credential is not provided.

Default setting (no value):
```
smb_usernameN: 
smb_passwordN:  
```
[top](#parameter-reference-guide)

### smb_pathN

!!! Note
    New for V2.1

The volume path to be used for SMB test number 'N' (1-N)

Default setting (no value):
```
smb_pathN: 
```
[top](#parameter-reference-guide)

### smb_filenameN

!!! Note
    New for V2.1

The filename to be used for SMB test number 'N' (1-N)

Default setting (no value):
```
smb_filenameN: 
```
[top](#parameter-reference-guide)

### smb_data_file

!!! Note
    New for V2.1

(Advanced setting, do not change) The name used for SMB the file/data group/data source.

Default setting (no value):
```
smb_data_file: 
```
[top](#parameter-reference-guide)
