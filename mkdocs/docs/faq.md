# FAQ

## How can I report a bug / ask a question / make a suggestion for wiperf?

Please checkout the [discussion section](https://github.com/wifinigel/wiperf/discussions) of the wiperf site of [GitHub](https://github.com/wifinigel/wiperf/discussions)

## Why do I get a message saying "Switch : failed wiperf mode" when I try to switch on to wiperf mode on the WLAN Pi?

In almost every instance, this is due to the fact that the configuration file for wiperf has not been configured before trying to switch in to wiperf mode.

Check out the required instructions here: [Probe configuration](https://wifinigel.github.io/wiperf/probe_configure/)

## When using wiperf on the WLAN Pi, how can I remotely flip between classic and wiper modes via the CLI?

**Warning** : Although it is possible to flip modes remotely (via an SSH session), be aware that you may hit network connectivity issues unless you are very careful. Remember that in classic mode the file `/etc/network/interfaces` and `/etc/wpa_supplicant/wpa_supplicant.conf` are used for network connectivity configuration. In wiperf mode, the files `/etc/wiperf/conf/etc/network/interfaces` and `/etc/wiperf/conf/etc/wpa_supplicant/wpa_supplicant.conf` are used for network connectivity configuration.

To check the current mode of the wiperf, enter the following command:

```
# this files shows the current mode state (i.e. wiperf, wconsole, hotspot or classic)
cat /etc/wlanpi-state
```

To check the current mode of wiperf using the wiper switcher script:

``` 
sudo /usr/bin/wiperf_switcher status
```

To toggle from classic mode to wiperf:

```
sudo /usr/bin/wiperf_switcher on
```

To toggle from wiperf mode to classic:

```
sudo /usr/bin/wiperf_switcher off
```

__(Remember, when switching modes, the wlanpi will reset and you will lose comms for around a minute)__



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

## How do I upgrade to the latest version of wiperf?
Please see the details in this page: [link](probe_upgrade.md)

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

## How can I fix my probe to only connect to one specific wireless access point for testing?

Checkout [this note](adv_fixed_bssid.md) for specific instructions on this configuration.

## Can I make a feature suggestion?
Yes, get along to the GitHub site and post your suggestion in the [discussion section](https://github.com/wifinigel/wiperf/discussions){target=_blank} of the wiperf GitHub site. It will be added to my "todo" list.

## Can I get some support with wiperf?
I try my best to support folks who are having difficulty, but it's a best efforts endeavour. Please make sure you checkout all of the documentation I've provided, but if all else fails, post a question in the [discussion section](https://github.com/wifinigel/wiperf/discussions){target=_blank} of the wiperf GitHub site. Please be patient...

## Can I contribute some code for a new feature for wiperf?
Please, get in touch before starting work on any code you'd like to submit as a PR. I love feedback and ideas, but each new feature costs me more cycles to support. Let's agree it can be included before submitting.

## Can I run tests over the Ethernet interface of the WLAN Pi?
Yes, from wiperf v2 onwards.
