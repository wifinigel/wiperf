Title: Quickstart
Authors: Nigel Bowden

# Quickstart Guide
<div style="float: right;">
![wiperf_logo](images/wiperf_logo.png)
</div>
Wiperf is a utility that can be installed on a [WLAN Pi](https://wlan-pi.github.io/wlanpi-documentation/) or a Raspberry Pi to act as a network probe that runs a series of  network performance tests. It is primarily intended to provide an indication of the end-user experience on a wireless network, but may also be used as an ethernet-connected probe.

Wiperf is a powerful solution, but it is not trivial to setup and configure. Here is a quickstart guide to outline the component parts and knowledge you'll need to get wiperf going.

__What it is:__ 

- an open source engineering tool that runs a set of network tests and reports in to a separate reporting tool (Splunk or Grafana) that is not part of the wiperf project. 
- Wiperf is *only* a probe that runs a series of network tests and makes data available to other tools.

__What it isn't:__ 

- An Enterprise quality/scale network monitoring tool
- A reporting tool
- A cheap way of providing Enterprise-wide UX monitoring

__Skills You'll Need:__ 
You will need to be comfortable with the following items to get wiperf going:

- Using SBC devices like the RPi and WLAN Pi (including burning images & getting on their CLI) 
- Basic Linux administration skills (including editing files on the CLI, running scripts, updating/adding packages)

__Building a Probe:__
You'll need to build the probe from scratch, which may include burning images on to an SD card, a variety of Linux operations such as adding new packages and performing administrative tasks such as setting the hostname, network configuration details and the timezone.

Once the basic probe is built, you will then download the wiperf code using an automated script and configure its operation using a CLI text editor.

__Reporting:__
As stated previously, wiperf __is not__ a reporting platform. It has been designed to send data to a reporting platform (that you build yourself, separately) such as Splunk or Grafana. 

Details are provided to "get you going" with the reporting platform, but these platforms are not part of this project and detailed customization of these platforms and supporting them is outside of the wiperf project. No support will be provided for these platforms besides the basic report templates that are provided on a best-efforts basis. 

Remember, wiperf is a UX network probe - analyzing the data it provides is your responsibility.

__Documentation:__
I have created a wide range of documentation to help you to get your wiperf probe going, together with the basics of setting up a suitable reporting platform. Please take time to read through this documentation before reaching out for support. 

I recommend that you start [here](operation.md) and work sequentially though the [documentation provided](operation.md).

