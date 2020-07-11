Title: Probe Deployment
Authors: Nigel Bowden

# Probe Deployment

TBA



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
