# wiperf

Wi-Fi performance probe

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
        sudo apt-get install python3-pip iperf3 git -y
        sudo reboot
```
     
Install required python3 modules

```
        sudo pip3 install iperf3 speedtest-cli configparser splunk-hec-handler
```

### User Account

Create the wlanpi user:
```
        sudo adduser wlanpi
```

Edit the sudoers file to enable the wlanpi user to run some commands that require elevated privilege:

```
        sudo visudo
```

- Add following line to bottom of file: 
```
        wlanpi  ALL=(ALL) NOPASSWD: ALL
```

Reboot and log back in with the wlanpi user:

```
        sudo reboot
```

### Wireless Configuration

Configure RPi to join a wireless network. Edit files 'sudo nano /etc/wpa_supplicant/wpa_supplicant.conf' and 'sudo nano /etc/network/interfaces'. The eth0 port is configured as static IP below, but can be left as dhcp if wlan0 & eth0 are on different networks (otherwise Speedtest traffic goes out of eth0 port)
(note: wpa_supplicant.conf must have root:root ownership - 'chown root:root /etc/wpa_supplicant/wpa_supplicant.conf' if required)

    *** Sample '/etc/wpa_supplicant/wpa_supplicant.conf':
    
        ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
        update_config=1
        country=GB
        ap_scan=1

        network={
                ssid="My_SSID"
                psk="My_SSID_Key"
                priority=1
                #freq_list=2412 2417 2422 2427 2432 2437 2442 2447 2452 2457 2462 2467 2472
                freq_list=5180 5200 5220 5240 5260 5280 5300 5320 5500 5520 5540 5560 5580 5600 5620 5640 5680 5700 5720 5745 5765 5785 5805 5625
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

Reboot RPi & verify the RPi has joined the wireless network with iwconfig/ifconfig 

## Installation

With the RPi connected to the Internet, login using the wlanpi user and clone this project:

```
        cd ~
        git clone https://github.com/wifinigel/wiperf.git
```

Edit the config file to customize the operation of the script:cd

```
        cp /home/wlanpi/wiperf/config.default.ini config.ini
        nano /home/wlanpi/wiperf/config.ini
```

### Testing

Test the script by running the following command (takes around 2 minutes to complete, depending on tests enabled):

```
        sudo /usr/bin/python3 /home/wlanpi/wiperf/wi-perf.py
```

If no errors are observed when running it then check the following files to check for no errors & that data is generated:
```    
        cat /home/wlanpi/wiperf/logs/agent.log
        cat /home/wlanpi/wiperf/data/wiperf-speedtest-splunk.csv
        cat /home/wlanpi/wiperf/data/wiperf-ping-splunk.csv
        cat /home/wlanpi/wiperf/data/wiperf-iperf3-udp-splunk.csv
        cat /home/wlanpi/wiperf/data/wiperf-iperf3-tcp-splunk.csv
```

## Running: Schedule Regular Job

Create a cronjob to run the script very 5 mins:

```
        sudo crontab -e
```

- add line: 
```
        */5 * * * * sudo /usr/bin/python3 /home/wlanpi/wiperf/wi-perf.py > /home/wlanpi/wiperf/wiperf.log 2>&1
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

- Run the script from the command line and watch for errors (sudo /usr/bin/python3 /home/wlanpi/wiperf/wi-perf.py)
- SSH to the device & tail the log files in real-time: tail -f /home/wlanpi/wiperf/logs/agent.log
- Try disabling tests & see if one specific test is causing an issue
- Make sure all pre-reqs have definitely been fulfilled
  
