

In this section, we'll walk through how to set up Wiperf on your WLAN Pi.

## How do I get Wiperf going on my WLAN Pi?

If you have a WLAN Pi with image version v1.9 or later, the good news is you're good to go! If not, you will need to update your WLAN Pi image (see this video on [YouTube][wlanpi_reimage]). Note: if you have the v1.9 image, you need to check this out and update the wiperf code before you start configuring wiperf: [FAQ note](#im-running-the-v19-wlan-pi-image-and-the-iperf-tests-dont-workwhats-going-on)

Assuming your image is up to date, you need to complete the following steps:

- Data Server:
    - Splunk: Setup your Splunk server and obtain the HEC token from your Splunk instance (see this doc: [Splunk build guide][splunk_build])
    - InfluxDB: Setup your InfluxDB server and a Grafana server to graph the performance data received.
- SSH to your WLAN Pi and configure your WLAN Pi as detailed in this guide: [WLANPi initial config & test guide][wlanpi_config]
- Flip your WLAN Pi in to wiperf mode and wait for your data to appear (Front panel option : Menu > Mode > Wiperf)