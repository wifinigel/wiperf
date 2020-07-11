# FAQ  (In development)

## How do I use wiperf with a proxy in my network?
TBA


## My probe only needs to hit internal network targets. How do I stop the connectivity check to google.com?
TBA


## How do I change the hostname of my probe?
TBA

## Why are MCS & Rx Phy rates missing from my reports?
In several dashboard reports, the reported MCS values & Rx Phy rate may be blank. This is because these values are only reported by MediaTek wireless NICs. Therefore, the CF-912 will not show these values (as it is a Realtek NIC). Sorry, not much I can do about this.

## My probe seems to reboot itself intermittently. Why?
Wiperf has a watchdog feature that it uses to try to reset things when it is having connectivity related difficulties.

There may be instances when tests are continually failing or wireless connectivity is intermittent due to perhaps being stuck on a remote AP that is sub-optimal from a connectivity perspective.

If persistent issues are detected, then wiperf will reboot the probe to try to remediate the issue. This will provide the opportunity to the reset all network connectivity and internal processes.

Note that this is a last ditch mechanism. Wiperf will try bouncing network interfaces to remediate any short-term connectivity issues, which will likely fix many issues without the need for a full reboot.

If you observe your probe rebooting on a regular basis (e.g. a couple of times a hour), then check its logs as it is very unhappy about something.

## Security

### WLAN Pi
Wiperf employs the following security mechanisms in an attempt to harden the WLAN Pi when deployed in Wiperf mode:

- No forwarding is allowed between interfaces
- The internal UFW firewall is configured to only allow incoming connectivity on port 22 on the wlan0 & eth0 interfaces

### RPi
TBA (suggest add ufw & apply rules)


## Where do I get the dashboard reports for Splunk and Grafana?
Use SFTP/SCP and pull the xml files in ```/usr/share/wiperf/dashboards``` from your probe. 

## Can I make a feature suggestion?

Yes, get along to the GitHub site and post your suggestion in the 'Issues' section: https://github.com/wifinigel/wiperf/issues. It will be added to my "todo" list.

## Can I run tests over the Ethernet interface of the WLAN Pi?
Yes, from wiperf v2.
