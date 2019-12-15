# Wiperf - Image Build Instructions for the WLANPi

Wi-Fi performance probe for RPi & WLANPi

## Pre-requisites

These are the build instuctions for the v1.8.5 WLANPi image:

### Package Updates

Update existing Linux packages:

```
        sudo apt-get update && sudo apt-get upgrade -y
        sudo reboot
```

Install required Linux packages:

```
        sudo apt-get update
        # WLANPi only: re-install python3 and python3-pip
        sudo apt-get --reinstall install python3
        sudo apt-get --reinstall install python3-pip
        sudo apt-get install python3-pip iperf3 git -y
        sudo reboot
```
     
Install required python3 modules

```
        sudo pip3 install iperf3 speedtest-cli configparser
        sudo pip3 install git+git://github.com/georgestarcher/Splunk-Class-httpevent.git
```

### User Account Permissions

Edit the sudoers file to enable the wlanpi user to run some commands that require elevated privilege:

```
        cd /etc/sudoers.d/
        sudo nano ./wlanpidump
```

change: 
```
        wlanpi ALL = (root) NOPASSWD: /sbin/iwconfig, /usr/sbin/iw
```
to:
```
        wlanpi ALL = (root) NOPASSWD: /sbin/iwconfig, /usr/sbin/iw, /bin/date, /sbin/dhclient, /sbin/ifconfig
```

Reboot and log back in with the wlanpi user:

```
        sudo reboot
```

## Installation

With the WLANPi/RPi connected to the Internet, login using the wlanpi user and clone this project:

```
        cd ~
        git clone https://github.com/wifinigel/wiperf.git --depth 1
```

At this point, the basic installation of the package is complete.
