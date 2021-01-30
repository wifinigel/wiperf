Title: About
Authors: Nigel Bowden

# About

![Probe Report](images/probe_summary.jpg)

Wiperf is a utility that can be installed on to a WLAN Pi or a Raspberry Pi to act as a network probe running a series of  network tests. It is primarily intended to provide an indication of the end-user experience on a wireless network, but may also be used as a standalone ethernet-connected probe.

The probe can run the following tests to give an indication of the performance of the network environment into which it has been deployed:

- Wireless connection health check (if wireless connected)
- Speedtest (Ookla/Librespeed)
- iperf3 (TCP & UDP tests)
- ICMP ping
- HTTP
- DNS
- DHCP
- SMB

Tests may be performed over the wireless or ethernet interface of the probe unit. The results must then be sent back to a Splunk or InfluxDB server (which we'll call the "data server") to provide a reporting capability. (*NOTE: There is no graphing/reporting capability on the wiperf probe itself*)

Wiperf has been primarily designed to be a tactical tool for engineers to deploy on to a wireless network where perhaps issues are being experienced and some longer term monitoring may be required. It is not designed to replace large-scale commercial offerings that provide wireless and end-user experience monitoring in a far more comprehensive and user-friendly fashion.



Tests are run on the wiperf probe at a configured interval (usually 5 minutes) and collected data is sent back to a data server over a network connection between the probe and data server (no connection = no data collection). The data server must be an instance of either:

- Splunk, or
- InfluxDB with Grafana  

## Developer

The primary developer for this project is Nigel Bowden. Check me out in the following places:

- [LinkedIn](https://www.linkedin.com/in/nigelbowden){target=_blank}
- [Twitter](https://twitter.com/wifinigel){target=_blank}
- [Blog](https://wifinigel.com){target=_blank}
