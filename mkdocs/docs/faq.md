# FAQ  (In development)

## How do I use wiperf with a proxy in my network?
If you need to deal with using a proxy on your network, please complete the details of your proxy by completing the following section in your ```/etc/wiperf/config.ini``` file:

```
; If proxy server access is required to run a speedtest, enter the proxy server details here for https & https
; e.g. https_proxy: http://10.1.1.1:8080
;
; For sites that are not accessed via proxy, use no_proxy (make sure value enclosed in quotes & comma separated for mutiple values)
; e.g. no_proxy: "mail.local, intranet.local"
http_proxy: 
https_proxy:
no_proxy:
```

## My probe only needs to hit internal network targets. How do I stop the DNS check to google.com?
Before commencing tests, wiperf will perform a test DNS lookup to ensure that DNS is working OK. By default, the DNS target in ```/etc/wiperf/config.ini``` is set to 'google.com'. If your DNS is internal to your network and does not resolve public Internet targets, yo can change the section below to point at an internal target.

```
; connectivity DNS lookup - site used for initial DNS lookup when assessing if DNS working OK
connectivity_lookup: google.com
```

## How do I change the hostname of my probe?
Please see the details in this help page: [link](probe_prepare.md)

## Why are MCS & Rx Phy rates missing from my reports?
In several dashboard reports, the reported MCS values & Rx Phy rate may be blank. This is because these values simply are not reported by many NICs. Sorry, there's not much I can do about this as I don't write the wireless NIC drivers.

## My probe seems to reboot itself intermittently. Why?
Wiperf has a watchdog feature that it uses to try to reset things when it is having connectivity related difficulties.

There may be instances when tests are continually failing or wireless connectivity is intermittent due to perhaps being stuck on a remote AP that is sub-optimal from a connectivity perspective.

If persistent issues are detected, then wiperf will reboot the probe to try to remediate the issue. This will provide the opportunity to the reset all network connectivity and internal processes.

Note that this is a last ditch mechanism. Wiperf will try bouncing network interfaces to remediate any short-term connectivity issues, which will likely fix many issues without the need for a full reboot.

If you observe your probe rebooting on a regular basis (e.g. a couple of times a hour), then check its logs as it is very unhappy about something.

## Security

### WLAN Pi
Wiperf employs the following security mechanisms in an attempt to harden the WLAN Pi when deployed in wiperf mode:

- No forwarding is allowed between interfaces
- The internal UFW firewall is configured to only allow incoming connectivity on port 22 on the wlan0 & eth0 interfaces

### RPi
If you'd like to harden the RPi when deployed in a network, a quick solution is to install & activate the 'ufw' firewall. This can be configured to stop all incoming connections except those on SSH, which will still allow remote administration. All outgoing traffic from the probe (i.e. network tests and management traffic) will not be disrupted.

#### Install ufw

```
apt-get update
apt-get install ufw
```

#### Add Firewall Rules

```
ufw allow in on eth0 to any port ssh
ufw deny in on eth0
ufw allow in on wlan0 to any port ssh
ufw deny in on wlan0
```

#### Activate Firewall
```
ufw enable
```

#### Useful Commands

```
# Disable the firewall comletely
ufw enable

# List fw rules with numbers
ufw status numbered

# See firewall status
ufw status
```

## Where do I get the dashboard reports for Splunk and Grafana?
Use SFTP/SCP and pull the xml files in ```/usr/share/wiperf/dashboards``` from your probe. 

## Can I make a feature suggestion?
Yes, get along to the GitHub site and post your suggestion in the 'Issues' section: https://github.com/wifinigel/wiperf/issues. It will be added to my "todo" list.

## Can I run tests over the Ethernet interface of the WLAN Pi?
Yes, from wiperf v2.
