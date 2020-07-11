Title: Probe Configuration
Authors: Nigel Bowden

# Probe Configuration  (In development - old version)
The final step in getting our probe ready to deploy is to configure the wiperf software to perform the tests we like to perform, and to tell wiperf where it can find the data server to provide reporting.

The configuration tasks break down as follows:

- Edit the config.ini file to configure tests and data server details
- Add a cron job to run wiperf every 5 mins to perform its tests


## Configuration File (config.ini)
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

; Platform architecture - choices: 'wlanpi' (WLPC WLAN-Pi),'rpi' (Raspberry Pi) 
platform: wlanpi
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

### Tests

Note that all network tests are enabled by default. If there are some tests you'd like to disable (e.g. if you don't have an iperf3 server set up), then you'll need to open up the config.ini file and look through each section for the "enabled" parameter for that test and set it to "no". For example, to disable the iperf tcp test: 

```
[Iperf3_tcp_test]
; yes = enabled, no = disabled
enabled: no
```

For a full description of the configuration file parameters, please review the following page: [config.ini reference guide](README_Config.ini.md). The Splunk token is obtained from your Splunk server (see [Splunk build guide][splunk_build]). 

[top](#contents)

## Wireless Client Configuration (wpa_supplicant.conf)

If Wiperf is running in wireless mode, then WLAN Pi is flipped in to Wiperf mode, it will need to join the SSID under test to run the configured tests. We need to provide a configuration (that is only used in Wiperf mode) to allow the WLAN Pi to join a WLAN.

Edit the following file with the configuration and credentials that will be used by the WLAN Pi to join the SSID under test once it is switched in to Wiperf mode (make edits logged in as the wlanpi user):

```
        cd /home/wlanpi/wiperf/conf/etc/wpa_supplicant
        nano ./wpa_supplicant.conf
```

[top](#contents)

## Ethernet Client Configuration

Note that no specific configuration is required for the Ethernet interface when running Wiperf in Ethernet mode. As long as the Ethernet port is connected to a switch port tht supplies an IP address via DHCP, then you're good to go. 

[top](#contents)

# Testing

Once the required edits have been made to configure Wiperf mode, flip the WLAN Pi in to Wiperf mode using the following FPMS options:

```
        Actions > Wiperf > Confirm
```

If no errors are observed on the FPMS during flip-over, inspect the following files to double-check for errors & verify that test data is generated (as indicated in the log messages):
```    
    cat /home/wlanpi/wiperf/logs/agent.log
    cat /home/wlanpi/wiperf/wiperf.log 
```
Note that by default the tests are run every 5 mins unless the interval has been changed in the `config.ini` file. Wait at least this interval before determining that there is an issue - the test cycle will NOT begin immediately upon entering Wiperf mode.

Check your database platform and verify that data is being received.

[top](#contents)


## Running: Schedule Regular Job

Create a cronjob to run the script very 5 mins:

```
        crontab -e
```

- add line: 
```
        */5 * * * * /usr/bin/env python3 /home/wlanpi/wiperf/wi-perf.py > /home/wlanpi/wiperf/wiperf.log 2>&1
```


