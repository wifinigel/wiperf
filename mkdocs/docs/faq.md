# FAQ  (In development - old version)

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
