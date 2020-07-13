Title: Security Hardening
Authors: Nigel Bowden

# Security Hardening

### WLAN Pi
Wiperf employs the following security mechanisms in an attempt to harden the WLAN Pi when deployed in wiperf mode:

- No forwarding is allowed between interfaces
- The internal UFW firewall is configured to only allow incoming connectivity on port 22 on the wlan0 & eth0 interfaces


### RPi
If you'd like to harden the RPi when deployed in a network, a quick solution is to install & activate the 'ufw' firewall. This can be configured to stop all incoming connections except those on SSH, which will still allow remote administration. All outgoing traffic from the probe (i.e. network tests and management traffic) will flow as normal.

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
