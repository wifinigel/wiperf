Title: Splunk Platform
Authors: Nigel Bowden

# Splunk Platform
<div style="float: right;">![splunk_logo](images/splunk_logo.png)</div>To collect and view the test results data, an instance of Splunk is required (unless you choose to use [InfluxDB/Grafana](influx_platform.md)). Splunk is a flexible data collection and reporting package that can take data sent by the wiperf probe and present it in a nice report format.  Splunk can be installed on a wide variety of platforms that can be viewed at : [https://www.splunk.com/en_us/download/splunk-enterprise.html](https://www.splunk.com/en_us/download/splunk-enterprise.html)

This guide does not cover all installation details of the software package, these may be obtained when downloading and installing the software. Note that a free account sign-up is required when downloading the software from the link listed above.

To install Splunk and use it with a handful of probes, a modest server may be built (e.g. I use a low-end Intel NUC running Ubuntu), so for testing purposes, don’t get too hung up on sourcing a high end server. If you'd like to look into server requirements further, then [check out this page](https://docs.splunk.com/Documentation/Splunk/latest/Installation/Systemrequirements).

The product being installed is Splunk Enterprise. This is a paid-for product, but it has a free-tier for low data volumes (500Mbytes per day). Install initially with all the licensing defaults and then drop back to the free-tier by selecting Settings > Licensing and selecting the free tier. The free tier is plenty for the low volume rates that the wiperf probe generates when deploying probes at small-scale.

!!! attention

    If you forget to select the free tier and your trial license expires, you may become locked out of the GUI with a “license expired” message. If this happens, from the CLI of your Splunk server, find the file “server.conf” and add the following line to the bottom of the file:

    ```
        [license]
        active_group = Lite_Free
    ```

    Then, restart the Splunk server and the login issue should be fixed.
    (The file is /opt/splunk/etc/system/local/server.conf on Linux)

## Connectivity Planning
One area to consider is network connectivity between the wiperf probe and the Splunk instance. The wiperf probe needs to be able to access the Splunk server to send its results data. If the wiperf probe probe is being deployed on a wireless network, how is the results data generated going to get back to the Splunk server?

If the probe is being deployed on a customer network to perform temporary monitoring, it will need to join the wireless network under test (or be plugged in to an ethernet switch port if testing a wired connection). But, how is the wiperf probe going to send its data to the Splunk server ? Many environments may not be comfortable with hooking up the wiperf probe to their internal wired network, potentially bridging wired and wireless networks. In some instances an alternative is required (e.g. send the results data over the wireless network itself out to the Internet to a cloud instance or via a VPN solution such as Zerotier.)

Three topology deployment options are supported:

- Results data over wireless
- Results data over Ethernet
- Results data over VPN/wireless 

The method used is configured on the wiperf probe in its config.ini file. It is important to understand the (viable) connectivity path prior to deploying both the probe and the Splunk server.

The 3 connectivity options are discussed below.

### Results Data Over Wireless

![splunk_wireless_mgt](images/splunk_wireless_mgt.png)

In this topology the wiperf probe is configured to join an SSID that has the Splunk server accessible via its WLAN interface. Typically, the Splunk server will reside in a cloud or perhaps on a publicly accessible VPS. The wiperf probe will continually run the performance tests over the wireless connection and then upload the results directly to the Splunk server over the WLAN connection.

!!! note "config.ini settings:"
    ```
    mgt_if: wlan0
    data_host: <public IP address of Splunk server> 
    ```

### Results data over Ethernet

![splunk_ethernet_mgt](images/splunk_ethernet_mgt.png)

If the Splunk server is being run on the inside of a network environment, it may be preferable to return results data via the Ethernet port of the wiperf probe. This topology also has the advantage of  results data not being impacted if there are wireless connectivity issues on the wiperf probe WLAN connection. To achieve the correct traffic flow, a static route for management traffic is automatically injected into the route table of the wiperf probe to force results data over the Ethernet port. 

!!! note "config.ini settings:"
    ```
        mgt_if: eth0
        data_host: <IP address of Splunk server> 
    ```


### Results data over Zerotier/wireless 

![splunk_zerotier_mgt](images/splunk_zerotier_mgt.png)

A simple way of getting the wiperf probe talking with your Splunk server, if it has no direct access, is to use the [Zerotier](https://zerotier.com/) service to create a virtual overlay network via the Internet.

In summary, both the Splunk server and wiperf probe have a [Zerotier](https://zerotier.com/) client installed. Both are then added to your Zerotier dashboard (by you) and they start talking! Under the hood, both devices have a new virtual network interface created and they connect to the [Zerotier](https://zerotier.com/) cloud-based network service so that they can communicate on the same virtual network in the cloud. As they are on the same subnet from a networking perspective, there are no routing issues to worry about to get results data from the wiperf probe to the Splunk server.

[Zerotier](https://zerotier.com/) has a free subscription tier which allows up to 100 devices to be hooked up without having to pay any fees. It’s very easy to use, plus your Splunk server can be anywhere! (e.g. on your laptop at home). Both devices need access to the Internet for this solution to work.

You can sign up for free, create a virtual network and then just add the IDs that are created by the Splunk server and wiperf probe when the client is installed.

!!! note "config.ini settings:"
    ```
        mgt_if: ztxxxxxx (check your local ZeroTier interface designation using ```ifconfig```)
        data_host: <IP address of Splunk server shown in Zerotier dashboard> 
    ```

!!! info "Install ZeroTier"

    To install Zerotier on the wiperf probe (or an Ubuntu server), enter the following:

    ```
        curl -s https://install.zerotier.com | sudo bash
        sudo zerotier-cli join <network number from your Zerotier dashboard>
        sudo zerotier-cli status

        # To remove at a later date:
        sudo apt remove zerotier-one
    ```
