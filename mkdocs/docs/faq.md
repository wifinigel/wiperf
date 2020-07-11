# FAQ  (In development - old version)

## Proxy


## Connectivity check (internal)



## I see bounce command error messages in the agent.log file, what is going on?

The following error messages may be seen in the agent.log file of wiperf if using the WLAN Pi v1.9.1 (or earlier) image:
```
ERROR - if bounce command appears to have failed. Error: sudo: no tty present and no askpass program specified
```
This occurs when connectivity issues are experienced and wiperf attempt to bounce the wireless interface to recover the wireless connection. To fix this issue, add the following entries to the /etc/sudoers.d/wlanpidump file:

```
/sbin/ifdown 
/sbin/ifup
```
The modified file content should be as follows:
```
wlanpi ALL = (root) NOPASSWD: /sbin/iwconfig, /usr/sbin/iw, /sbin/dhclient, /sbin/ifconfig, /sbin/reboot, /bin/kill, /bin/date, /sbin/ifdown, /sbin/ifup
```
This will ensure that the wireless interface may be correctly bounced by wiperf if required.

## DNS Lookup Order Issue

By default in WLAN Pi image versions up to and including v1.9.1, the DNS server value ```8.8.8.8``` has been hard-coded in to the DNS server lookup list. This has been achieved by configuring the following line in to the file ```/etc/resolvconf/resolv.conf.d/head```:

```
nameserver 8.8.8.8
```
This ensures that the 8.8.8.8 address is always used as the first DNS lookup entry, even if the WLAN Pi receives a DNS server address during its DHCP process. This can be verified by performing a ```cat /etc/resolv.conf``` when the WLAN Pi is in wiperf mode - even though there may be two or more entries in the file, 8.8.8.8 will always be shown at the top of the file listing, and be used as the first lookup server. This may not be desirable behaviour, as 8.8.8.8 may not be available or DHCP assigned servers may be preferred. 

To ensure that the desired DNS environment is used, the following options exist:

1. Remove the 8.8.8.8 entry completely: edit the file  ```/etc/resolvconf/resolv.conf.d/head``` and remove the offending entry completely. This will ensure only the DHCP assigned DNS server(s) will be used.
2. Replace the 8.8.8.8 entry by editing the  ```/etc/resolvconf/resolv.conf.d/head``` and replacing it with a desired value
3. Move the 8.8.8.8 entry from the ```/etc/resolvconf/resolv.conf.d/head``` file to the ```/etc/resolvconf/resolv.conf.d/tail``` file, so that 8.8.8.8 is still used, but is now the last option in the DNS server list (only used when other preceding servers do not return a result)

[top](#contents)


## MCS & Rx Phy rates Missing From Reports

[top](#contents)

In several dashboard reports, the reported MCS values & Rx Phy rate may be blank. This is because these values are only reported by MediaTek wireless NICs. Therefore, the CF-912 will not show these values (as it is a Realtek NIC). Sorry, not much I can do about this.

[top](#contents)

## Tests Fail To Start Due to DNS Failures

In versions of wiperf before version v0.10, the wiperf probe performed a series of tests to verify the health of the wireless connection prior to tests running. One of these tests included a DNS lookup to "bbc.co.uk" to verify Internet connectivity.

In some environments, this may not be a valid test. To fix this issue, a new configuring parameter was added to the config.ini file that allows a custom lookup target to be provided, if requried: 
```
connectivity_lookup: google.com
```

[top](#contents)



[top](#contents)

# Additional Features:

## Watchdog

Wiperf has a watchdog feature that it uses to try to reset things when it is having connectivity related difficulties.

There may be instances when tests are continually failing or wireless connectivity is intermittent due to perhaps being stuck on a remote AP that is sub-optimal from a connectivity perspective.

If persistent issues are detected, then Wiperf will reboot the WLAN Pi to try to remediate the issue. This will provide the opportunity to the reset all network connectivity and internal processes.

Note that this is a last ditch mechanism. Wiperf will try bouncing the WLAN interface to remediate any short-term connectivity issues, which will likely fixe many issues without the need for a full reboot.

If you observe your WLAN Pi rebooting on a regular basis (e.g. a couple of times a hour), then check its logs as it is very unhappy about something.

[top](#contents)

## Security

Wiperf employs the following security mechanisms in an attempt to harden the WLAN Pi when deployed in Wiperf mode:

- No forwarding is allowed between interfaces
- The internal UFW firewall is configured to only allow incoming connectivity on port 22 on the wlan0 & eth0 interfaces

[top](#contents)


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
