# FAQ

## Why does installation of wiperf fail with the message "(fail) pip installation of wiperf_poller failed. Exiting." ?
This is usually due to the fact that the version of python required for wiperf is python version 3.7 or greater. This means that python version 3.7, 3.8...etc are fine but 3.6, 3.5, 3.4, 3.3... etc. will not work.

To check the version of python on your probe, enter the CLI command: ```python -V``` (note the uppercase 'V').

If you cannot upgrade your version of python using "apt-get", then you will need to obtain a more recent image for your probe.

## How do I use wiperf with a proxy in my network?
Please see this advanced configuration note: [link](adv_proxy.md)

## My probe only needs to hit internal network targets. How do I stop the DNS check to google.com?
Before commencing tests, wiperf will perform a test DNS lookup to ensure that DNS is working OK. By default, the DNS target in ```/etc/wiperf/config.ini``` is set to 'google.com'. If your DNS is internal to your network and does not resolve public Internet targets, you can change the section below to point at an internal lookup target (that will pass a lookup!).

```
; connectivity DNS lookup - site used for initial DNS lookup when assessing if DNS working OK
connectivity_lookup: google.com
```

## How do I change the hostname of my probe?
Please see the details in this help page: [link](probe_prepare.md)

## Why are MCS & Rx Phy rates missing from my reports?
In several dashboard reports, the reported MCS values & Rx Phy rate may be blank or permanently zero. This is because these values simply are not reported by many NICs. Sorry, there's not much I can do about this as I don't write the wireless NIC drivers.

## My probe seems to reboot itself intermittently. Why?
Wiperf has a watchdog feature that it uses to try to reset things when it is having connectivity related difficulties.

There may be instances when tests are continually failing or wireless connectivity is intermittent due to perhaps being stuck on a remote AP that is sub-optimal from a connectivity perspective.

If persistent issues are detected, then wiperf will reboot the probe to try to remediate the issue. This will provide the opportunity to the reset all network connectivity and internal processes.

Note that this is a last ditch mechanism. Wiperf will also try bouncing network interfaces to remediate any short-term connectivity issues, which will likely fix many issues without the need for a full reboot.

If you observe your probe rebooting on a regular basis (e.g. a couple of times a hour), then check its logs as it is very unhappy about something.

## How Can I Harden the Probe Security?
Please see this note for some suggestions for hardening the probe: [link](adv_secure.md)


## Where do I get the dashboard reports for Splunk and Grafana?
Use SFTP/SCP and pull the xml files in ```/usr/share/wiperf/dashboards``` from your probe. Or, visit the wiperf GitHub site [here](https://github.com/wifinigel/wiperf/tree/main/dashboards){target=_blank}

## Can I make a feature suggestion?
Yes, get along to the GitHub site and post your suggestion in the ['Issues' section](https://github.com/wifinigel/wiperf/issues){target=_blank}. It will be added to my "todo" list.

## Can I run tests over the Ethernet interface of the WLAN Pi?
Yes, from wiperf v2 onwards.
