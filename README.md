# wiperf

Wi-Fi performance probe for RPi & WLANPi

## Pre-requisites

### Package Updates

Update existing Linux packages:

```
        sudo apt-get update && sudo apt-get upgrade -y
        sudo reboot
```

Install required Linux packages:

```
        sudo apt-get update
        # WLANPi only: re-install python3 and python3-pip (not req on RPi)
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

### User Account

Create the wlanpi user (only required on the RPi):
```
        sudo adduser wlanpi
```

**RPi Only**: Edit the sudoers file to enable the wlanpi user to run some commands that require elevated privilege:

```
        sudo visudo
```

- Add following line to bottom of file: 
```
        wlanpi  ALL=(ALL) NOPASSWD: ALL
```

**WLANPi Only**: Edit the sudoers file to enable the wlanpi user to run some commands that require elevated privilege:

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
        wlanpi ALL = (root) NOPASSWD: /sbin/iwconfig, /usr/sbin/iw, /sbin/dhclient
```

**Both platforms**: Reboot and log back in with the wlanpi user:

```
        sudo reboot
```

### Wireless Configuration

Configure WLANPi/RPi to join a wireless network. Edit files 'sudo nano /etc/wpa_supplicant/wpa_supplicant.conf' and 'sudo nano /etc/network/interfaces'. The eth0 port is configured as static IP below, but can be left as dhcp if wlan0 & eth0 are on different networks (otherwise Speedtest traffic goes out of eth0 port)
(note: wpa_supplicant.conf must have root:root ownership - 'chown root:root /etc/wpa_supplicant/wpa_supplicant.conf' if required)

    *** Sample '/etc/wpa_supplicant/wpa_supplicant.conf':
    
        ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
        update_config=1
        ap_scan=1

        network={
                ssid="My_SSID"
                psk="My_SSID_Key"
        }
    
    *** Sample '/etc/network/interfaces':
    
        # interfaces(5) file used by ifup(8) and ifdown(8)

        # Please note that this file is written to be used with dhcpcd
        # For static IP, consult /etc/dhcpcd.conf and 'man dhcpcd.conf'

        auto wlan0
        allow-hotplug wlan0
        iface wlan0 inet dhcp
        wpa-conf /etc/wpa_supplicant/wpa_supplicant.conf

        # Note eth0 has been set to a static address to avoid routing issues 
        # when both eth0 and wlan0 are on same network (traffic goes out of 
        # eth0 rather than wlan0). If they are on different networks, it's
        # OK to set eth0 to DHCP, but may still need a static route to force
        # Internet-bound traffic to use wlan0 rather than eth0
        auto eth0
        allow-hotplug eth0 
        # iface eth0 inet dhcp 
        iface eth0 inet static
        address 192.168.254.1
        netmask 255.255.255.0

        # Local loopback
        auto lo
        iface lo inet loopback

        # Include files from /etc/network/interfaces.d:
        source-directory /etc/network/interfaces.d/*

Reboot WLANPi/RPi & verify the it has joined the wireless network with iwconfig/ifconfig 

## Installation

With the WLANPi/RPi connected to the Internet, login using the wlanpi user and clone this project:

```
        cd ~
        git clone https://github.com/wifinigel/wiperf.git
```

Edit the config file to customize the operation of the script:

```
        cd /home/wlanpi/wiperf
        cp ./config.default.ini ./config.ini
        nano ./config.ini
```

### Testing

Test the script by running the following command (takes around 2 minutes to complete, depending on tests enabled):

```
        /usr/bin/python3 /home/wlanpi/wiperf/wi-perf.py
```

If no errors are observed when running it then check the following files to check for no errors & that data is generated:
```    
        cat /home/wlanpi/wiperf/logs/agent.log
        # (Note: none of the files below are created when using the HEC forwarder )
        cat /home/wlanpi/wiperf/data/wiperf-speedtest-splunk.json
        cat /home/wlanpi/wiperf/data/wiperf-ping-splunk.json
        cat /home/wlanpi/wiperf/data/wiperf-iperf3-udp-splunk.json
        cat /home/wlanpi/wiperf/data/wiperf-iperf3-tcp-splunk.json
        .
        .
        etc...
```

## Running: Schedule Regular Job

Create a cronjob to run the script very 5 mins:

```
        crontab -e
```

- add line: 
```
        */5 * * * * /usr/bin/python3 /home/wlanpi/wiperf/wi-perf.py > /home/wlanpi/wiperf/wiperf.log 2>&1
```
## Account Tidy-up

If this has been built using a new RPI image, remember to either update the default 'pi' username with a new password, or remove the account. Make sure you have successfully logged in with the 'wlanpi' user and are using it to perform the operations shown below.

- Change password : sudo passwd pi
- Remove account: sudo userdel pi

## Updating

To get the latest updates from the GitHub repo , use the following commands when logged in as the wlanpi user:

```
        cd ~/wiperf
        git pull https://github.com/wifinigel/wiperf.git
```

(note that this will update config.default.ini but not config.ini, or remember to re-edit it after a pull if the format changes)

## Troubleshooting:

If things seem to be going wrong, try the following:

- Run the script from the command line and watch for errors (/usr/bin/python3 /home/wlanpi/wiperf/wi-perf.py)
- SSH to the device & tail the log files in real-time: tail -f /home/wlanpi/wiperf/logs/agent.log
- Try disabling tests & see if one specific test is causing an issue
- Make sure all pre-reqs have definitely been fulfilled
  
