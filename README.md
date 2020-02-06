# wiperf

Wiperf is a utility that can be installed on to a WLAN Pi or a Raspberry Pi to act as a network probes running a series of  network tests. It is primarily intended to provide an indication of the end-user experience on a wireless network.

It can run tests to an iperf server or to the Ookla speedtest service to give an indication of what network throughput looks like. While running tests, the probe also gathers information about wireless connection data.

Additionally, the probe can be configured to run a number of ping, DNS and http tests to chosen targets.

![Probe Report][probe_image]

Tests are run at a configured interval (usually 5 minutes) and data is sent back to a Splunk server (which will need to be setup and configured separately). The volume of data returned by the probe is very low, so the free tier of Splunk may be used to gather and report on data. To find out how to setup a Splunk server, check out this document: [Splunk build guide][splunk_build] (it's a lot easier than you might expect...honestly)

Wiperf has been designed to be a tactical tool for engineers to deploy on to a wireless network where perhaps issues are being experienced and some longer term monitoring may be required. It is not designed to replace large-scale commercial offerings that provide wireless and end-user experience monitoring in a far more comprehensive and user-friendly fashion.



# Documentation

The current documentation for Wiperf is available below. This documentation is subject to regular updates as new features are added.

## WLANPi Docs

- [WLANPi initial config & test guide][wlanpi_config]
- [config.ini reference guide][config_ini]
- [Splunk build guide][splunk_build]
- [WLANPi Image Build Guide for Wiperf (image devs only)][wlanpi_build]


## RPI Docs

- [RPI software installation and setup overview][rpi_readme]

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
