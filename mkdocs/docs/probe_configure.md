Title: Probe Configuration
Authors: Nigel Bowden

# Probe Configuration
The final step in getting our probe ready to deploy is to configure the wiperf software to perform the tests we'd like to perform, and to tell wiperf where it can find the data server that will provide reporting.

The configuration tasks break down as follows:

- Edit the probe config.ini file to configure tests and data server details
- Add a cron job on the probe to run wiperf every 5 mins to perform its tests


## Configuration File
*Note: the details in this section apply to both the WLAN Pi and RPi probe*

The operation of wiperf is configured using the file ```/etc/wiperf/config.ini``` This needs to be edited prior to running the wiperf software to perform tests. (Tests are initiated on the WLAN Pi by switching on to wiperf mode. On the RPi, tests are started by configuring a cron job - more on this later in this document)

Prior to the first use of wiperf, the config.ini file does not exist. However, a default template config file (```/etc/wiperf/config.default.ini```) is supplied that can be used as the template to create the `config.ini` file. Here is the suggested workflow to create the ```config.ini``` file:

Connect to the CLI of the probe (e.g. via SSH), create a copy of the config template file and edit the newly created config:

```
cd /etc/wiperf
cp ./config.default.ini ./config.ini
sudo nano ./config.ini
```

By default, the configuration file is set to run all tests (which may or may not suit your needs). However, there is a minimum configuration that must be applied to successfully run tests. The minimum configuration parameters you need to configure (just to get you going) are outlined in the subsections below. Once you've got your probe going, you're likely going to want to spend a little more time customising the file for your environment. In summary you need to:

* Configure the wiperf global mode of operation (wireless or Ethernet) and the interface parameters that determine how the probe is connected to its network
* Configure the management platform you'll be sending data to
* Configure the tests you'd like to run

### Mode/Interface Parameters
The probe can be used to perform its tests over its wireless interface, or its ethernet interface. These are known as 'wireless' or 'ethernet' mode in the config.ini file. 

In addition, the probe needs to know which interface is used to send results data back to the data server. It is possible to perform tests and send results data over the same interface, or it may be preferable to have tests performed over the wireless interface and return results over the ethernet interface. The final choice is determined by the environment in to which the probe is deployed.

(Note: if you choose to use Zerotier for management connectivity, the Zerotier interface is also an option available).

The interfaces available in the probe for ethernet and wireless connectivity will generally be ```eth0``` and ```wlan0```. However, these may vary in some platforms, there the option to change the actual names of the interfaces of the probe is available if required.

The relevant section of the config.ini file is shown below for reference (note that lines that start with a semi-colon (;) are comments and are ignored. Blank lines are also ignored.):

```
[General]
; global test mode: 'wireless' or 'ethernet'
; 
; wireless mode: 
;    - test traffic runs over wireless interface
;    - management traffic (i.e. result data) sent over interface specified in mgt_if parameter
; ethernet mode:
;    - test traffic runs over ethernet interface
;    - management traffic (i.e. result data) sent over interface specified in mgt_if parameter
;
probe_mode: wireless

; ------------- ethernet mode parameters ------------
; eth interface name - set this as per the output of an ifconfig command (usually eth0)
eth_if: eth0
; ---------------------------------------------------

; ------------- wireless mode parameters ------------
; wlan interface name - set this as per the output of an iwconfig command (usually wlan0)
wlan_if: wlan0
; ---------------------------------------------------

; -------------mgt interface parameters ------------
; interface name over which mgt traffic is sent (i.e. how we get to our management
; server) - options: wlan0, eth0, ztxxxxxx (ZeroTier), lo (local instance of Influx)
mgt_if: wlan0
; ---------------------------------------------------
```
### Data Server Parameters

Wiperf can send results data to Splunk and InfluxDB (v1.x) data collectors through an exporter module for each collector type. The relevant authentication parameters need to be set for the collector in-use in the following sections (note these also need to be configured on the data collector platform also before sending results data - see here for more info: [Splunk](splunk_configure.md) / [InfluxDB](influx_configure.md))

In summary, the workflow to configure the data server parameters in the probe configuration file is to:

- Set the exporter type (splunk/influxdb)
- configure the server address of the target data server
- configure data server port details (if defaults changed)
- configure data server credential and database information

The relevant section of the ```config.ini``` file is shown below:

```
; --------- Common Mgt Platform Params ------- 
; set the data exporter type - current options: splunk, influxdb, influxdb2
exporter_type: splunk
; --------------------------------------------

; -------------- Splunk Config ---------------
; IP address or hostname of Splunk host
splunk_host: 
; Splunk collector port (8088 by default)
splunk_port: 8088
; Splunk token to access Splunk server created by Splunk (example token: 84adb9ca-071c-48ad-8aa1-b1903c60310d)
splunk_token: 
;---------------------------------------------

; -------------- InFlux1 Config ---------------
; IP address or hostname of InfluxDB host
influx_host: 
; InfluxDb collector port (8086 by default)
influx_port: 8086
influx_username: 
influx_password: 
influx_database: 
;---------------------------------------------
```

### Network Tests

Note that all network tests are enabled by default. If there are some tests you'd like to disable (e.g. if you don't have an iperf3 server set up), then you'll need to open up the config.ini file and look through each section for the "enabled" parameter for that test and set it to "no". For example, to disable the iperf tcp test: 

```
[Iperf3_tcp_test]
; yes = enabled, no = disabled
enabled: no
```

For a full description of the configuration file parameters, please review the following page: [config.ini reference guide](config.ini.md){target=_blank}. 


## Running Regular Tests
Once the wiperf software has been configured, the final job is to configure a 'cron job' on the probe to run the software every 5 minutes. Cron is a scheduler utility within Linux that will run a software task at configured intervals.

(__Note: This step is not required on the WLAN Pi, as the cron job is added automatically when the WLAN Pi is switched in to wiperf mode__)

To configure cron, on the CLI of the probe, open the cron editor:

```
sudo crontab -e
```

Next, with the editor open, add following line to the open file: 
```
0-59/5 * * * * /usr/bin/python3 /usr/share/wiperf/wiperf_run.py > /var/log/wiperf_cron.log 2>&1
```
This command will run the main wiperf script to run the tests configured within config.ini at an interval of 5 minutes. It will also dump all script output to the file  ```/var/log/wiperf_cron.log``` (this is a good place to look if you hit any issues with wiperf not running as expected)

## Initial Probe Testing
Once the cron job has been configured, the case of the RPi, or the WLAN Pi has been put in to wiperf mode, it's time to check if the probe is working as expected.

To perform tests, the probe will need to be connected to a network and able to reach the data server.

The easiest way to monitor the operation of the probe is to SSH in to the probe and monitor the output of the log file ```/var/log/wiperf_agent.log```. This file is created the first time that wiperf runs. If the file is not created after 5 minutes, then check the log file ```/var/log/wiperf_cron.log``` for error messages, as something fundamental is wrong with the installation.

To watch the output of ```/var/log/wiperf_agent.log``` in real-time and view activity as data is collected every 5 minutes, run the following command on the CLI of the probe:

```
tail -f /var/log/wiperf_agent.log
```

Every 5 minutes, new log output will be seen that look similar to this:

```
2020-07-11 11:47:04,214 - Probe_Log - INFO - *****************************************************
2020-07-11 11:47:04,215 - Probe_Log - INFO -  Starting logging...
2020-07-11 11:47:04,216 - Probe_Log - INFO - *****************************************************
2020-07-11 11:47:04,240 - Probe_Log - INFO - Checking if we use remote cfg file...
2020-07-11 11:47:04,241 - Probe_Log - INFO - No remote cfg file confgured...using current local ini file.
2020-07-11 11:47:04,242 - Probe_Log - INFO - No lock file found. Creating lock file.
2020-07-11 11:47:04,243 - Probe_Log - INFO - ########## Network connection checks ##########
2020-07-11 11:47:05,245 - Probe_Log - INFO - Checking wireless connection is good...(layer 1 &2)
2020-07-11 11:47:05,246 - Probe_Log - INFO -   Checking wireless connection available.
2020-07-11 11:47:05,355 - Probe_Log - INFO - Checking we're connected to the network (layer3)
2020-07-11 11:47:05,356 - Probe_Log - INFO -   Checking we have an IP address.
2020-07-11 11:47:05,379 - Probe_Log - INFO -   Checking we can do a DNS lookup to google.com
2020-07-11 11:47:05,406 - Probe_Log - INFO -   Checking we are going to Internet on correct interface as we are in 'wireless' mode.
2020-07-11 11:47:05,430 - Probe_Log - INFO -   Checked interface route to : 216.58.212.238. Result: 216.58.212.238 via 192.168.0.1 dev wlan0 src 192.168.0.48 uid 0
2020-07-11 11:47:05,431 - Probe_Log - INFO - Checking we can get to the management platform...
2020-07-11 11:47:05,432 - Probe_Log - INFO -   Checking we will send mgt traffic over configured interface 'lo' mode.
2020-07-11 11:47:05,455 - Probe_Log - INFO -   Checked interface route to : 127.0.0.1. Result: local 127.0.0.1 dev lo src 127.0.0.1 uid 0
2020-07-11 11:47:05,456 - Probe_Log - INFO -   Interface mgt interface route looks good.
2020-07-11 11:47:05,457 - Probe_Log - INFO -   Checking port connection to InfluxDB server 127.0.0.1, port: 8086
2020-07-11 11:47:05,484 - Probe_Log - INFO -   Port connection to server 127.0.0.1, port: 8086 checked OK.
2020-07-11 11:47:05,485 - Probe_Log - INFO - ########## Wireless Connection ##########
2020-07-11 11:47:05,486 - Probe_Log - INFO - Wireless connection data: SSID:BNL, BSSID:5C:5B:35:C8:4D:C2, Freq:5.5, Center Freq:5.51, Channel: 100, Channel Width: 40, Tx Phy rate:200.0,             Rx Phy rate:135.0, Tx MCS: 0, Rx MCS: 0, RSSI:-42.0, Tx retries:187, IP address:192.168.0.48
2020-07-11 11:47:05,486 - Probe_Log - INFO - InfluxDB update: wiperf-network, source=Network Tests
2020-07-11 11:47:05,487 - Probe_Log - INFO - Sending data to Influx host: 127.0.0.1, port: 8086, database: wiperf)
2020-07-11 11:47:05,573 - Probe_Log - INFO - Data sent to influx OK
2020-07-11 11:47:05,574 - Probe_Log - INFO - Connection results sent OK.
2020-07-11 11:47:05,595 - Probe_Log - INFO - ########## speedtest ##########
2020-07-11 11:47:05,597 - Probe_Log - INFO - Starting speedtest...
2020-07-11 11:47:06,599 - Probe_Log - INFO -   Checking we are going to Internet on correct interface as we are in 'wireless' mode.
2020-07-11 11:47:06,623 - Probe_Log - INFO -   Checked interface route to : 8.8.8.8. Result: 8.8.8.8 via 192.168.0.1 dev wlan0 src 192.168.0.48 uid 0
2020-07-11 11:47:06,624 - Probe_Log - INFO - Speedtest in progress....please wait.
2020-07-11 11:47:28,761 - Probe_Log - INFO - ping_time: 31, download_rate: 41.56, upload_rate: 9.74, server_name: speedtest-net5.rapidswitch.co.uk:8080
2020-07-11 11:47:28,766 - Probe_Log - INFO - Speedtest ended.
2020-07-11 11:47:28,767 - Probe_Log - INFO - InfluxDB update: wiperf-speedtest, source=Speedtest
2020-07-11 11:47:28,768 - Probe_Log - INFO - Sending data to Influx host: 127.0.0.1, port: 8086, database: wiperf)
2020-07-11 11:47:28,858 - Probe_Log - INFO - Data sent to influx OK
2020-07-11 11:47:28,860 - Probe_Log - INFO - Speedtest results sent OK.
```

The output is quite verbose and detailed, but it will provide a good indication of where wiperf is having difficulties.

Once wiperf is running with no issues indicated in the logs, then it's time to check for results data on your data server. Hopefully, you'll see performance data being recorded over time as the probe runs its tests and sends the results to the data server. 