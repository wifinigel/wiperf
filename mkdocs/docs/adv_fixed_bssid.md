Title: Configuring a Fixed Access Point
Authors: Nigel Bowden

# Configuring the Probe to Test Against Only One Access Point

There may be instances when there is a requirement to ensure that the wiperf probe connects only to a specific wireless access point (AP). In an environment where there are multiple APs that broadcast the same SSID (network name), the probe may roam between different access points over time (which is normal 802.11 operation)

If you like to ensure that the probe never moves from a specific AP, you will need to add a "BSSID" address to the wiperf probe supplicant file. (Note: if the AP ever becomes unavailable, the probe will be stranded without comms as it will not roam to another AP, even if it broadcasts the same network name)

When an AP broadcasts an SSID (i.e. the network name), it will use a specific "BSSID" for that network name, which is effectively a unique MAC address for that network name.  To fix the probe to use only one specific AP, you will need to find the BSSID of the network name to which you would like it fixed. If you use a wireless network scanner tool, it will generally show you SSID names and their associated BSSIDs (MAC addresses).

Once you have obtained the BSSID you need, this needs to be added to the `/etc/wpa_supplicant/wpa_supplicant.conf` file for the RPI, or the `/etc/wiperf/conf/etc/wpa_supplicant/wpa_supplicant.conf` file for the WLAN Pi.

Here is an simple example configuration file that shows the BSSID configuration parameter being used - note the `"bssid"` configuration parameter:

```
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=GB

network={
        ssid="My_Home_Network"
        psk="s3cret_pwd"
        bssid=01:23:45:67:89:ab
}
```

After setting this new configuration parameter, reboot the probe to ensure it is used by the wireless interface of the probe. 