
# Troubleshooting

If things seem to be going wrong, here are a few tips to guide you in your diagnosis of the issue.

## Network Connectivity

If you suspect network connectivity issues, your best course of action is to check the status of any interfaces being used by the probe. This can be done by accessing the CLI of the probe and running some of the commands provided below.

Once interfaces have been verified, trying to access specific targets via network connectivity checks can also be useful. 

1. The following CLI commands will help to check the status of probe interfaces:
    1. Wireless NIC: ```iwconfig``` (Is the probe joining the wireless network? The SSID to which is is joined should be shown in the "ESSID" field)
    2. IP address: ```ifconfig eth0```, ```ifconfig wlan0``` (Are the interfaces up? Do they have an IP address?)
2. Network connectivity to a specific host: ```ping 192.168.0.254```
3. Internet connectivity: ```ping google.com``` (Can the probe get to the Internet, if that is expected?)
4. DNS connectivity: ```apt-get install dnsutils``` (install required commands), ```nslookup google.com```
5. Web connectivity: ```wget https://google.com``` (check if the required website target can be reached from the probe)
6. iperf3 server connectivity: ```iperf3 -c 192.168.0.1 -t 10 -i 1``` (run 10 sec tcp test to 192.168.0.1 server...alter for your iperf server address)
7. Another useful source of information for connectivity issues in the syslog logging system of the probe. Take a look through the syslog file to see if there are any issues being reported that may be impacting your connectivity: ```tail -f /var/log/syslog```

## Wiperf Configuration
The wiperf configuration file is quite a complex file, so it's well worth checking for typos or critical fields that have been missed. The key fields worth double checking are:

- probe_mode
- mgt_if
- exporter_type
- (splunk)
    - splunk_host
    - splunk_port
    - splunk_token
- (influxdb)
    - influx_host
    - influx_port
    - influx_username
    - influx_password
    - influx_database

One question to consider when deploying a probe is : Is the probe deployed in the topology you originally intended? If the environment is not as you expected and you need to use a different interface, make sure you have updated ```config.ini``` so that wiperf knows where to send test and management traffic (otherwise, you may hit routing issues)

## Logging
Wiperf has extensive logging to help diagnose issues that may be causing operational issues.

SSH to the probe and monitor the output of the log file ```/var/log/wiperf_agent.log```. This file is created the first time that wiperf runs. If the file is not created after 5 minutes, then check the log file ```/var/log/wiperf_cron.log``` for error messages, as something fundamental is wrong with the installation.

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

## Miscellaneous Checks

### NTP / Time Sync
Make sure your probe and reporting server are time synchronized and are showing the same data and time. Check the time and date of the probe using the CLI command `date`. If your probe and reporting server are in different timezones, check the UTC time on both to make sure you are comparing apples with apples: `date -u`

The WLAN Pi and RPi will generally synchronized to a time source out of the box using a process such as Chrony or NTP, so will not need any specific intervention. However, if they do not have access to the Internet, the synchronization process may be compromised and may need you to [manually configure time sources](https://pimylifeup.com/using-ntp-on-linux-with-chrony/){target=_blank}.

### Hostname
If you have changed the probe hostname from its default, make sure you have updated both the `/etc/hosts` **AND** the `/etc/hostname` files with the new name (if done incorrectly, this can cause some very weird issues!)


