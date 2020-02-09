# wiperf

Wiperf is a utility that can be installed on to a WLAN Pi or a Raspberry Pi to act as a network probe running a series of  network tests. It is primarily intended to provide an indication of the end-user experience on a wireless network.

It can run tests to an iperf server or to the Ookla speedtest service to give an indication of what network throughput looks like. While running tests, the probe also gathers information about wireless connection data.

Additionally, the probe can be configured to run a number of ping, DNS and http tests to chosen targets.

The probe attempts to perform all tests over the wireless interface of the WLAN Pi. The results may be sent back to the Splunk server over the wireless or ethernet interface of the WLAN Pi. If you're wondering how to get the results back to your Splunk server and its not on the customer network, or maybe you don't have a cloud/VPS instance to run it on, check out "Zerotier" in the  [Splunk build guide][splunk_build] (yes...you can have the Splunk server on your desk at work or at home!)

![Probe Report][probe_image]

Tests are run at a configured interval (usually 5 minutes) and data is sent back to a Splunk server (which will need to be setup and configured separately). The volume of data returned by the probe is very low, so the free tier of Splunk may be used to gather and report on data. To find out how to setup a Splunk server, check out this document: [Splunk build guide][splunk_build] (it's a lot easier than you might expect...honestly)

Wiperf has been designed to be a tactical tool for engineers to deploy on to a wireless network where perhaps issues are being experienced and some longer term monitoring may be required. It is not designed to replace large-scale commercial offerings that provide wireless and end-user experience monitoring in a far more comprehensive and user-friendly fashion.

# Setting up Wiperf

In this section, we'll walk through how to set up Wiperf on your WLAN Pi.

## How do I get Wiperf going on my WLAN Pi?

If you have a WLAN Pi with image version v1.9 or later, the good news is you're good to go! If not, you will need to update your WLAN Pi image (see this video on [YouTube][wlanpi_reimage]). Note: if you have the v1.9 image, you need to check this out and update the wiperf code before you start configuring wiperf: [FAQ note](#im-running-the-v19-wlan-pi-image-and-the-iperf-tests-dont-workwhats-going-on)

Assuming your image is up to date, you need to complete the following steps:

- Setup your Splunk server and obtain the HEC token from your Splunk instance (see this doc: [Splunk build guide][splunk_build])
- SSH to your WLAN Pi and configure your WLAN Pi as detailed in this guide: [WLANPi initial config & test guide][wlanpi_config]
- Flip your WLAN Pi in to wiperf mode and wait for your data to appear (Front panel option : Menu > Mode > Wiperf)

![HTTP Report][http_image]

## How do I troubleshoot issues I may be having?

Check out the troubleshooting section of this guide: [WLANPi initial config & test guide][wlanpi_config]

# FAQ

## Where do I get the dashboard reports for Splunk?

Use SFTP/SCP and pull the xml files in /home/wlanpi/wiperf/dashboards from your WLAN Pi. See the [Splunk build guide][splunk_build] for details of how to add them to Splunk.

## The dashboard reports show no MCS data and RX PHY rate data - why not?

Various WLAN NICs that use both Realtek and Mediatek WLAN chips are now supported by the WLAN Pi. Unfortunately, the Realtek chipsets (e.g. our old favourite the CF-912) do not report as much data as the Mediatek chips, so this data is missing. As I am not aware of any way of making the dashboard reports show data conditional on the chipset used, some graphs are shown but not fully populate - sorry.

## How do I get more reports or customize the supplied Splunk reports?

Sorry, you'll have to roll up your sleeves and have a look at this for yourself: https://docs.splunk.com/Documentation/Splunk/8.0.1/SearchTutorial/Createnewdashboard

## Can I make a feature suggestion?

Yes, get along to the GitHub site and post your suggestion in the 'Issues' section: https://github.com/wifinigel/wiperf/issues. It will be added to my "todo" list.

## Can I run tests over the Ethernet interface of the WLAN Pi?

No, not at present. It was originally designed as a WLAN test device, so I need to do a bit of code re-writing to get tests going over Ethernet. Stay tuned.

## I'm running the v1.9 WLAN Pi image and the iperf tests don't work....what's going on?

There was an issue with the code distributed with image v1.9. Try the following:

- ssh to the WLAN Pi
- Run the following commands (assuming the WLAN Pi has Internet connectivity):

```
cd ~/wiperf
git pull https://github.com/wifinigel/wiperf.git
```

(It's best to do this is classic mode and redo you Wiperf configuration again after this operation - note that the config.default.ini file has new options you will probably like to use. Don't forget to check /home/wlanpi/wiperf/config/etc/wpa_supplicant/wpa_supplicant.conf too.)

# Documentation

The current documentation for Wiperf is available below.

## WLANPi Docs

- [WLAN Pi initial config & test guide][wlanpi_config]
- [config.ini reference guide][config_ini]
- [Splunk build guide][splunk_build]
- [WLAN Pi Image Build Guide for Wiperf (image devs only)][wlanpi_build]
- [WLAN Pi Documentation Site][doc_site]


## RPI Docs

- [RPI software installation and setup overview][rpi_readme]

![Speedtest Report][speedtest_image]

<!-- link list -->
[rpi_readme]: docs/README_RPi.md
[wlanpi_build]: docs/README_WLANPi_Image_Build.md
[wlanpi_config]: docs/README_WLANPi_Config.md
[config_ini]: docs/README_Config.ini.md
[splunk_build]: https://github.com/wifinigel/wiperf/raw/master/docs/WLANPi%20Wiperf%20Probe%20-%20Splunk%20Build.pdf
[http_image]: https://github.com/wifinigel/wiperf/raw/master/docs/images/http_summary.JPG
[iperf_image]: https://github.com/wifinigel/wiperf/raw/master/docs/images/iperf_summary.JPG
[probe_image]: https://github.com/wifinigel/wiperf/raw/master/docs/images/probe_summary.JPG
[speedtest_image]: https://github.com/wifinigel/wiperf/raw/master/docs/images/speedtest_summary.JPG
[wlanpi_reimage]: https://www.youtube.com/watch?v=sD4WlNyyWDs
[doc_site]: https://wlan-pi.github.io/wlanpi-documentation/
[license]: License.txt

# Credits

Thanks to [Kristian Roberts](https://uk.linkedin.com/in/krisalexroberts) for his invaluable input, testing and guidance on Splunk. He kicked this whole thing off and it definitely wouldn't have happened without him. A top bloke.

# Caveats

This free software is provided for you to use at your own risk. There are no guarantees around its operation, suitability or the data that it provides. Please consult the [license file][license] shipped with this software.

# Developer

Nigel Bowden (WifiNigel): https://twitter.com/wifinigel
