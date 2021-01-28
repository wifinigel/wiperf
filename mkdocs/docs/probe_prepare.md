Title: Probe Preparation
Authors: Nigel Bowden

# Probe Preparation

The wiperf probe needs to have a few pre-requisite activities completed prior to the installation of wiperf code. These vary slightly between the WLAN Pi and RPi platforms, but broadly break down as:

- Software image preparation
- Obtain CLI Access
- Configure the device hostname
- Configure network connectivity
- Add pre-requisite software packages.

__Choose the Instructions for your probe type:__

- [Go to WLAN Pi instructions](#wlan-pi)
- [Go to Raspberry Pi instructions](#raspberry-pi)

## WLAN Pi

### Software Image
There is little to do in terms of software image preparation for the WLAN Pi. Visit the WLAN Pi documentation site to find out how to obtain the WLAN Pi image: [link](https://wlan-pi.github.io/wlanpi-documentation/){target=_blank}. If you install a WLAN Pi image, wiperf will already be installed as part of the image. (Note: *all information provided below assumes you are using a 2.0 or later version of the WLAN Pi image*)

### Probe CLI Access
To perform some of the configuration activities required, CLI access to the WLAN Pi is required. The easiest way to achieve this is to SSH to the probe over an OTG connection, or plug the WLAN Pi in to an ethernet network port and SSH to its DHCP assigned IP address (shown on the front panel). Visit the WLAN Pi documentation site for more details of how to gain access to the WLAN Pi: [link](https://wlan-pi.github.io/wlanpi-documentation/){target=_blank}

### Hostname Configuration
By default, the hostname of your WLAN Pi is : ```wlanpi```. It is strongly advised to change its hostname if you have several probes reporting in to the same data server. If all use the same hostname, there will be no way of distinguishing data between devices. 

*(Note that if you decide to skip this step and subsequently change the hostname, historical data from the probe will not be associated with the data sent with the new hostname in your data server)*

If you'd like to change to a more meaningful hostname, then you will need to SSH to your WLAN Pi and update the ```/etc/hostname``` and ```/etc/hosts``` files, followed by a reboot of the WLAN Pi:

Edit the /etc/hostname file using the command:

```
sudo nano /etc/hostname
```

There is a single line that says 'wlanpi'. Change this to your required hostname. Then hit Ctrl-X  and "y" to save your changes.

Next, edit the /etc/hosts file:

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
If the probe is to be connected to Ethernet only, then there is no additional configuration required. By default, if a switch port that can supply a DHCP address is used, the probe will have the required network connectivity.

#### Wireless Configuration (wpa_supplicant.conf)
If wiperf is running in wireless mode, when the WLAN Pi is flipped in to wiperf mode, it will need to join the SSID under test to run the configured network tests. We need to provide a configuration (that is only used in wiperf mode) to allow the WLAN Pi to join a WLAN.

Edit the following file with the configuration and credentials that will be used by the WLAN Pi to join the SSID under test once it is switched in to wiperf mode:

```
cd /etc/wiperf/conf/etc/wpa_supplicant
sudo nano ./wpa_supplicant.conf
```

There are a number of sample configurations included in the default file provided (PSK, PEAP & Open auth). Uncomment the required section and add in the correct SSID & authentication details. (For EAP-TLS, it's time to check-out Google as I've not had opportunity to figure that scenario out...)

(__Note:__ *This wireless configuration is only used when the WLAN Pi is flipped in to wiperf mode, not for standard (classic mode) wireless connectivity*)

!!! Note
    If you'd like to fix the AP that the probe associates with, check out [this note](adv_fixed_bssid.md)

At this point, the pre-requisite activities for the WLAN Pi are complete. Next, move on to the [probe configuration](probe_configure.md).

## Raspberry Pi

### Software Image
I would strongly recommend starting with a fresh image using the latest and greatest Raspberry Pi OS (previously called Raspbian): [https://www.raspberrypi.org/downloads/raspberry-pi-os/](https://www.raspberrypi.org/downloads/raspberry-pi-os/){target=_blank}. I would also recommend that you use the "headless", Lite version of Raspberry Pi OS rather than the desktop version (this is mainly as I have not tested with the desktop version and am not sure if there will be any resource or package conflict issues.)

__Note:__ *A Python version of 3.6 or greater is required to wiperf. The Python version installed as part of the distribution you are using used must be Python 3.6 or higher (check with ```python3 -V```). Going with a recent RPi image is strongly advised to ensure this requirement is met*

__Note:__ *Please use a dedicated RPi platform that is used only as a probe. Please do not install additional packages other than those recommended. Also, please use only one active Ethernet interface and one active wireless interface. Multiple live adapters will likely cause operational issues.*

For the development and testing of the wiperf code, version 10 (Buster) was used. You can check the version on your RPi using the ```cat /etc/os-release``` command. Here is my sample output:

```
pi@probe7:~$ cat /etc/os-release 
PRETTY_NAME="Raspbian GNU/Linux 10 (buster)"
NAME="Raspbian GNU/Linux"
VERSION_ID="10"
VERSION="10 (buster)"
VERSION_CODENAME=buster
ID=raspbian
ID_LIKE=debian
HOME_URL="http://www.raspbian.org/"
SUPPORT_URL="http://www.raspbian.org/RaspbianForums"
BUG_REPORT_URL="http://www.raspbian.org/RaspbianBugs"
```

Note that you will likely be able to use any recent version, so don't feel compelled to use this exact version.

The download page provided above also has links to resources to guide you through how to burn the fresh image on to your SD card. (*You may also like to check out the ['Probe CLI Access'](#probe-cli-access) section below to setup SSH access to your headless RPI before booting from your new image*) 

Once you have burned your image, I'd also recommend you apply all latest updates & give it a reboot for good measure:

```
sudo apt-get update && sudo apt-get upgrade
sudo reboot
```

### Probe CLI Access
You will need CLI access to perform the required configuration steps for wiperf. There are a number of ways of gaining this access that are detailed in this document: [https://www.raspberrypi.org/documentation/remote-access/ssh/](https://www.raspberrypi.org/documentation/remote-access/ssh/){target=_blank} (see the section *"Enable SSH on a headless Raspberry Pi"*). 

My personal favourite is to enable SSH on a headless RPi by adding an 'ssh' file to the SD card prior to boot-up (see section *"Enable SSH on a headless Raspberry Pi"* in the link above).

#### Default Login Account Password
If using a fresh RPI image (which is recommended), remember to update the default 'pi' username with a new password so that your are not running with the default login of : ```pi/raspberry``` (user/pwd)

- Change password : ```sudo passwd pi```


### Set Country Code
If you're starting with a freshly burned image for your RPi, the country code for your internal Wi-Fi adapter needs to be configured before it will activate. To configure the country code. Enter the following on the RPi CLI:

```
sudo raspi-config
```

A textual menu system will open and the following options need to be selected to set the country code: ```4. Localization Options > I4 Change WLAN Country > <Select Country> > OK > Finish```

(Note that if this step is not completed, your wireless adapter will likely not work)

### Hostname Configuration
By default, the hostname of your RPi is : ```raspberrypi```. It is strongly advised to change its hostname if you have several probes reporting in to the same data server. If all use the same hostname, there will be no way of distinguishing data between devices.

*(Note that if you decide to skip this step and subsequently change the hostname, historical data from the probe will not be associated with the data sent with the new hostname in your data server)*

If you'd like to change this to a more meaningful hostname, then you will need to SSH to your RPi and update the ```/etc/hostname``` and ```/etc/hosts``` files, followed by a reboot of the RPi:

Edit the /etc/hostname file using the command:

```
 sudo nano /etc/hostname
```

There is a single line that says 'raspberrypi'. Change this to your required hostname. Then hit Ctrl-X  and "y" to save your changes.

Next, edit the /etc/hosts file:

```
 sudo nano /etc/hosts
```
Change each instance of 'raspberrypi' to the new hostname (there are usually two instances). Then hit Ctrl-X  and "y" to save your changes.

Finally, reboot your RPi:

```
 sudo reboot
```

### Network Connectivity

__Note:__ *Use the method below to configure network interfaces. DO NOT use the RPI desktop GUI to configure network connectivity (if using the desktop RPi image, which is not recommended anyhow)....it will definitely __not__ work if configured via the GUI network utility.*

#### Ethernet
If the RPi is to be connected by Ethernet you will need to make some additions to the `/etc/network/interfaces` file to ensure you have network connectivity. Add the following lines to configure the Ethernet port for DHCP connectivity (unless they already exist in the file):

```
 # Wired adapter #1
 allow-hotplug eth0
 iface eth0 inet dhcp
```

These lines may be added anywhere in the file, using a CLI editor such as nano:

```
 sudo nano /etc/network/interfaces
```

#### Wireless Configuration
The RPi needs to be configured to join the wireless network that you'd like to test (assuming you want to test over a wireless connection - omit this step if you are testing wired only). To join a network, we need to configure the wireless interface and provide the network credentials to join the network. To achieve this, we need to edit two files via the CLI of the RPI:

```
/etc/wpa_supplicant/wpa_supplicant.conf
/etc/network/interfaces
```

Sample configurations for both files are provided below. 

##### /etc/network/interfaces

```
# configure the interfaces file
sudo nano /etc/network/interfaces
```

Sample config:

```
# wiperf interface config file

# Wired adapter #1
allow-hotplug eth0
iface eth0 inet dhcp

# Wireless adapter #1
allow-hotplug wlan0
iface wlan0 inet dhcp
wpa-conf /etc/wpa_supplicant/wpa_supplicant.conf
# wireless-power off
# post-up iw dev wlan0 set power_save off

```

__Note:__ *The wireless power off commands are commented out in the file above. One of these generally needs to be uncommented to stop the wireless NIC dropping in to power save mode. If you see huge drops in the wireless connection speed in the wireless connection graph, it is being caused by power save mode. Unfortunately, the command to use seems to vary between RPi model and operating system version. When you see the connection speed issue, try uncommenting one of the commands and reboot. If it doesn't fix the issue, try the other command. (see this [article for more info](https://www.kalitut.com/2017/11/turn-off-power-saving-mode-of-wlan.html){target=_blank})*

##### /etc/wpa_supplicant/wpa_supplicant.conf

Editing this file will provide the credentials required to join the wireless network under test:

```
# edit wpa_supplicant.conf file
sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
```

Sample config:

```
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
# Note the country code below will be likey be different, depending on what was set using raspi-config
country=GB
ap_scan=1

# WPA2 PSK Network sample (highest priority - joined first)
network={
  ssid="enter SSID Name"
  psk="enter key"
  priority=10
}

#######################################################################################
# NOTE: to use the templates below, remove the hash symbols at the start of each line
#######################################################################################

# WPA2 PSK Network sample (next priority - joined if first priority not available) - don't unhash this line

#network={
#    ssid="enter SSID Name"
#    psk="enter key"
#    priority=3
#}

# WPA2 PEAP example (next priority - joined if second priority not available) - don't unhash this line

#network={
#  ssid="enter SSID Name"
#  key_mgmt=WPA-EAP
#  eap=PEAP
#  anonymous_identity="anonymous"
#  identity="enter your username"
#  password="enter your password"
#  phase2="autheap=MSCHAPV2"
#  priority=2
#}

# Open network example (lowest priority, only joined other 3 networks not available) - don't unhash this line

#network={
#   ssid="enter SSID Name"
#   key_mgmt=NONE
#   priority=1
#}
```
Note that the file includes several samples for a variety of security methods. You will need to uncomment the network section that corresponds to the security method for your environment and comment out all other methods. By default, the PSK method is used (and uncommented), but requires that you enter an SSID and shared key. 

##### Test Wireless Connection

Once configuration is complete, reboot the RPI:

```
sudo reboot
```

To test if the wireless connection has come up OK, use the following commands to see if wireless interface has joined the wireless network and has an IP address (checkout the info for wlan0 - does it show an ESSID name (your network) and have an IP address?):

```
sudo iwconfig
sudo ifconfig
```

!!! Note
    If you'd like to fix the AP that the probe associates with, check out [this note](adv_fixed_bssid.md)

Next, we need to [install a few software packages on to the RPi probe](probe_install.md#raspberry-pi).
