Title: Results Data Caching
Authors: Nigel Bowden

# Results Data Caching

!!! Note
    __New in V2.1__

There were a number of requests from folks for results data to be made available on the local file system of the wiperf probe, in addition to being forwarded to a reporting platform. To meet these requests, results caching has been implemented.

This feature is disabled by default, but when enabled all test results are stored on the local file system in either CSV or JSON format. To limit the amount of local file storage consumed, a maximum age limit is configured to age-out older date and prevent the local file system filling up. Note that test results are still sent to the configured reporting platform when caching is enabled.

The data files are stored in the local directory `/var/cache/wiperf` for a configurable period of time (*3 days by default*).

A new day-specific directory is created each day, with a data file for each test type being run (example folder listing below):

```
root@rpi3a:/var/cache/wiperf/2021-01-15# ls -l
total 40
-rw-r--r-- 1 root root  98 Jan 15 21:12 wiperf-dhcp.csv
-rw-r--r-- 1 root root 279 Jan 15 21:11 wiperf-dns.csv
-rw-r--r-- 1 root root 472 Jan 15 21:11 wiperf-http.csv
-rw-r--r-- 1 root root 252 Jan 15 21:12 wiperf-iperf3-tcp.csv
-rw-r--r-- 1 root root 255 Jan 15 21:12 wiperf-iperf3-udp.csv
-rw-r--r-- 1 root root 512 Jan 15 21:11 wiperf-network.csv
-rw-r--r-- 1 root root 616 Jan 15 21:11 wiperf-ping.csv
-rw-r--r-- 1 root root 634 Jan 15 21:12 wiperf-poll-status.csv
-rw-r--r-- 1 root root 451 Jan 15 21:12 wiperf-smb.csv
-rw-r--r-- 1 root root 484 Jan 15 21:11 wiperf-speedtest.csv
```

The day-specific folder (and all of its data) is removed once its age exceeds the defined age-out threshold.

If only subset of results need to be cached, then they can be filtered using the `cache_filter` [configuration field](config.ini.md#cache_filter).

## Configuration

This feature is enabled and configured via the usual wiperf configuration file: `/etc/wiperf/config.ini`. The relevant section of the file is shown below:

```
; ====================================================================
;  General settings - any changes to this section should only be
;  made when in classic mode (not while in wiperf mode) on the WLAN Pi
; ====================================================================
[General]
;
; !!!!!!!!!!!!!!!!! SNIP !!!!!!!!!!!!!!!!!!!!!!!!!!!
;
; ----------- Caching Parameters -------------
; Results data may be cached in the local file system
; of the probe for later inspection or retrieval by
; user defined methods. By default, files are stored
; in: /var/cache/wiperf
;
; Enable/disable local file caching (yes or no)
cache_enabled: no
; Format of local cache files (csv or json)
cache_data_format: csv
; Number of days of data that will be retained
; local cache files 
cache_retention_period: 3
; data source filter (e.g. to cache only http & ping data: wiperf-http, wiperf-ping)
cache_filter:
;---------------------------------------------
```

Each of the configuration parameters are detailed in the [config.ini reference document](config.ini.md#cache_enabled).

Note that this data cannot be exported to a reporting server, it is only provided for local inspection or remote retrieval by some other user-defined method.

## Example Output

Here is a very brief sample of output data in CSV format for ping tests:
```
root@rpi3a:/var/cache/wiperf/2021-01-15# cat wiperf-ping.csv 
time,ping_index,ping_host,pkts_tx,pkts_rx,percent_loss,test_time_ms,rtt_min_ms,rtt_avg_ms,rtt_max_ms,rtt_mdev_ms
1610744198240,1,google.com,10,10,0,21,16.4,22.12,35.05,5.25
1610744207526,2,cisco.com,10,10,0,22,132.56,139.05,157.93,7.84
1610744497522,1,google.com,10,10,0,22,17.2,21.42,37.68,5.86
1610744506813,2,cisco.com,10,10,0,22,132.64,155.31,297.98,47.96
1610744798459,1,google.com,10,10,0,22,18.2,22.38,33.54,4.92
1610744807743,2,cisco.com,10,10,0,22,132.23,138.41,158.16,8.22
```
