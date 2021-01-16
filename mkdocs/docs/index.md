Title: Wiperf V2 Documentation
Authors: Nigel Bowden

# wiperf V2: An Open Source UX Performance Probe
<div style="float: left;">
![wiperf_logo](images/wiperf_logo.png)
</div>
![wiperf hardware](images/hardware.png)

Wiperf is a utility that can be installed on a [WLAN Pi](https://wlan-pi.github.io/wlanpi-documentation/) or a Raspberry Pi to act as a network probe that runs a series of  network performance tests. It is primarily intended to provide an indication of the end-user experience on a wireless network, but may also be used as an ethernet-connected probe.

The probe can run the following tests to give an indication of the performance of the network environment into which it has been deployed:

- Wireless connection health check (if wireless connected)
- Speedtest (Ookla/Librespeed)
- iperf3 (TCP & UDP tests)
- ICMP ping
- HTTP
- DNS
- DHCP
- SMB

Tests may be performed over the wireless or ethernet interface of the probe unit. The results must then be sent back to a Splunk or InfluxDB server (which we'll call the "data server") to provide a reporting capability. (*NOTE: There is ([usually](adv_rpi_standalone.md)) no graphing/reporting capability on the wiperf probe itself*)

Wiperf has been primarily designed to be a tactical tool for engineers to deploy on to a wireless network where issues are being experienced and longer term monitoring may be required. It is not designed to replace large-scale commercial offerings that provide wireless and end-user experience monitoring in a far more comprehensive and user-friendly fashion.

![Probe Report](images/probe_summary.jpg)

Tests are run on the wiperf probe at a configured interval (usually 5 minutes) and collected data is sent back to a data server over a network connection between the probe and data server (no connection = no data collection). The data server must be an instance of either:

- Splunk, or
- InfluxDB with Grafana  

## Data Server
The core focus of this project is the probe device that gathers the network performance data in which we are interested. However, the data server is a critical component that allows visualization of that performance data.  High-level configuration details will be provided to "get you going", but detailed information about the operation of these platforms is beyond the scope of this project.

Both of the data servers supported are "NoSQL" servers, which means that no data structures have to be pre-defined in database tables. This means we can send our data structures, that contain network performance data, to the server with very little set-up compared to traditional database servers.

As long as we have a valid set  of credentials for the data server, we can just send JSON-formatted data over HTTPS in whatever structure we choose. A database query language on the data server allows us to retrieve and graph the data collected by the wiperf probe.

### Splunk
Splunk is supported on all popular operating systems and is very easy to set up on your server of choice. It acts as both the data store and visualization platform. Splunk is a commercial, rather than open-source product.

The volume of data returned by the probe is very low, so the free tier of Splunk may be used to gather and report on data. For details on how to set up a Splunk server, start at this documentation page: [link][splunk_platform.md]

- Splunk product web site: [https://www.splunk.com/](https://www.splunk.com/)

### InfluxDB/Grafana

Grafana is a popular open-source data visualization tool. It is used to graph the performance data collected by wiperf. However, Grafana needs a data server from which to pull its network performance data. To meet this requirement, the InfluxDB database server is used. Like Grafana, InfluxDB is also an open-source package.

For small-scale instances, Grafana & Influx may be installed on the same server platform and Grafana configured to use the local instance of Influx as its data source.

- Grafana web site (v6.7): [https://grafana.com/](https://grafana.com/)
- Influx web site (v.1.8): [https://www.influxdata.com](https://www.influxdata.com)

## Workflow to Setup Wiperf

The workflow to get Wiperf fully operational consists of a number of steps that break down in to two main areas:

- Probe setup (the RPi or WLAN Pi device itself)
- Data server setup (the Splunk or Influx/Grafana server)

The data server setup tends to be a task that needs completion only once (or at least very infrequently). 

Conversely, some or all of the probe setup will need to be completed each time a probe is deployed - this is mainly due to the fact that in each environment in which it is deployed, the connectivity for the probe will vary (e.g. different SSID, different network connection type etc.). 

Here is an overview of the workflow::

- Data server setup:
    - Prepare a server platform
    - Obtain the data server application software
    - Install the data server application(s)
    - Configure the data server application(s)
- Probe setup:
    - Obtain a probe device (Raspberry Pi or WLAN Pi)
    - Prepare the device for the wiperf software
    - Install the wiperf software
    - Configure the wiperf software
    - Deploy & test the wiperf probe

__Links:__

- Start here for Splunk: [link](splunk_platform.md)
- Start here for InfluxDB/Grafana: [link](influx_platform.md)
- Start here for the probe: [link](probe_platform.md)

In addition to the setup and deployment of the components, there may also be a requirement to troubleshoot the setup. The following pages provide useful support information:

- [Troubleshooting steps](troubleshooting.md)
- [Review known issues / FAQ](faq/md)]

## Further Documentation References

- [Configuration file parameters](config.ini.md)
- [Data points sent by the probe to the data server platform](data_points.md)


![Speedtest Report](images/speedtest_summary.jpg)

## Credits
This project has had some great input from a number of people. Here are a few words of thanks to those who have been so generous in helping out.

Thanks to [Kristian Roberts](https://uk.linkedin.com/in/krisalexroberts) for his invaluable project input, testing and guidance on Splunk. He kicked this whole thing off and it definitely wouldn't have happened without him. A top bloke.

Thanks also to Eric Garnel and James Whitehead for their invaluable help in providing me so many Grafana dashboard files to "borrow" from. It was a steep learning curve for me, but the generosity of Eric & James really helped me to get to grips with Grafana. Also thanks to Eric for providing the idea to use InfluxDB as a data source (....even if I did use the wrong version initially! Lol). 

The code for the MOS score calculation was kindly provided by Mario Gingras. What a great idea...I wish I'd thought of that! Thanks Mario, it's great addition.

## Caveats
This free software is provided for you to use at your own risk. There are no guarantees around its operation, suitability or accuracy of the data that it provides. Please consult the [license file](https://github.com/wifinigel/wiperf/blob/main/License.txt) shipped with this software.

## Developer
Nigel Bowden (WifiNigel):

- (https://wifinigel.blogspot.com)[https://wifinigel.blogspot.com]{target=_blank}
- (https://github.com/wifinigel)[https://github.com/wifinigel]{target=_blank}



