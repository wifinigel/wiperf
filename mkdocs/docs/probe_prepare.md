Title: Probe Preparation
Authors: Nigel Bowden

# Probe Preparation

The wiperf probe needs to have a few pre-requisite activities completed prior to the installation of the wiperf code. These vary slightly between the WLAN Pi and RPi platforms, but broadly break down as:

- Configure the device hostname
- Configure network connectivity
- Add pre-requisite software packages.

## WLAN Pi

### Hostname Configuration

By default, the hostname of your WLAN Pi is : ```wlanpi```. It is strongly advised to change the hostname of your WLAN Pi if you have several probes reporting in to the same data server. If all use the same hostname, there will be no way of distinguishing data between devices. 

If you'd like to change this to a more meaningful hostname, then you will need to SSH to your WLAN Pi and update the ```/etc/hostname``` and ```/etc/hosts``` files, followed by a reboot of the WLAN Pi:

Edit the /etc/hostname file using the command:

```
 sudo nano /etc/hostname
```

There is a single line that says 'wlanpi'. Change this to your required hostname. Then hit Ctrl-X  and "y" to save your changes.

Alternatively, you may also use the following CLI command to achieve the same result:

```
sudo hostnamectl set-hostname <name>
```

Whichever method is used to update the hostname file, next edit the /etc/hosts file:

```
 sudo nano /etc/hosts
```
Change each instance of 'wlanpi' to the new hostname (there are usually two instances). Then hit Ctrl-X  and "y" to save your changes.

Finally, reboot your WLAN Pi:

```
 sudo reboot
```
### Network Connectivity

#### Ethernet

If the probe is to be connected by Ethernet only, then there is no additional configuration required. By default, if a switch port that can supply a DHCP address is used, then the probe will have the required network connection.

#### Wireless Configuration (wpa_supplicant.conf)

If wiperf is running in wireless mode, then when the WLAN Pi is flipped in to wiperf mode, it will need to join the SSID under test to run the configured tests. We need to provide a configuration (that is only used in wiperf mode) to allow the WLAN Pi to join a WLAN.

Edit the following file with the configuration and credentials that will be used by the WLAN Pi to join the SSID under test once it is switched in to wiperf mode:

```
        cd /etc/wiperf/conf/etc/wpa_supplicant
        sudo nano ./wpa_supplicant.conf
```

(Note: This configuration is only used when the WLAN Pi is flipped in to wiperf mode, not for standard (classic mode) connectivity)

## Raspberry Pi

### Hostname Configuration

By default, the hostname of your WLAN Pi is : ```pi```. It is strongly advised to change the hostname of your RPi if you have several probes reporting in to the same data server. If all use the same hostname, there will be no way of distinguishing data between devices. 

If you'd like to change this to a more meaningful hostname, then you will need to SSH to your WLAN Pi and update the ```/etc/hostname``` and ```/etc/hosts``` files, followed by a reboot of the RPi:

Edit the /etc/hostname file using the command:

```
 sudo nano /etc/hostname
```

There is a single line that says 'pi'. Change this to your required hostname. Then hit Ctrl-X  and "y" to save your changes.

Alternatively, you may also use the following CLI command to achieve the same result:

```
sudo hostnamectl set-hostname <name>
```

Whichever method is used to update the hostname file, next edit the /etc/hosts file:

```
 sudo nano /etc/hosts
```
Change each instance of 'pi' to the new hostname (there are usually two instances). Then hit Ctrl-X  and "y" to save your changes.

Finally, reboot your RPi:

```
 sudo reboot
```

### Network Connectivity

#### Ethernet

If the probe is to be connected by Ethernet only, then there is no additional configuration required. By default, if a switch port that can supply a DHCP address is used, then the probe will have the required network connection.

#### Wireless Configuration

Configure RPi to join a wireless network. Edit files 'sudo nano /etc/wpa_supplicant/wpa_supplicant.conf' and 'sudo nano /etc/network/interfaces'. The eth0 port is configured as static IP below, but can be left as dhcp if wlan0 & eth0 are on different networks (otherwise Speedtest traffic goes out of eth0 port)
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

Reboot the RPi & verify the it has joined the wireless network with iwconfig/ifconfig 

