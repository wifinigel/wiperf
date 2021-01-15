Title: SMB/CIFS Test
Authors: Nigel Bowden

# SMB/CIFS Test

!!! Note
    __New in V2.1__

The SMB/CIFS benchmarking test performs a simple copy of a file from a server to the local wiperf host. This may be useful to simulate a standard Windows file copy from a server.

Once each test is completed, data is reported that shows the file copied, the transfer time and the data rate achieved. Note that transfers that take longer than one minute will time out, so please consider this when setting up tests.

Up to 5 tests may be performed during each wiperf poll cycle. For each test, the following information must be configured:

* smb_host: name of IP of he remote server
* smb_username: username for login credentials on remote server 
* smb_password: password for login credentials on remote server 
* smb_path: the shared remote server path 
* smb_filename: the remote file to be copied during the test

(See the following reference document for more detailed configuration information: [config.ini](config.ini.md#smb_test-section)

## Pre-requisites

As the SMB/CIFS test suite is an optional test module, some prerequisite linux packages may be missing from your wiper probe software (both WLAN Pi and RPi). 

To ensure that you have the required packages on your wiper probe, please run the following commands:

```
sudo apt-get update
sudo apt-get install cifs-utils
```

If you get a message advising that `cifs-utils` is already installed, do not worry.

## Configuration

Once the pre-requisite packages are installed, as with all other wiperf tests, please configure the relevant section of the wiperf probe `/etc/wiperf/config.ini` file. Please visit this document for detail information about the configuration options: [config.ini](config.ini.md#smb_test-section))


## General SMB Testing (Supplementary Info)
If you are not too familiar with using SMB/CIFS file shares and would like to set up and perform your own testing (e.g. in your lab), here are some useful notes on setting up a basic SMB server and client using some test Linux devices. __Note:__ *these are unsupported reference notes which may/may not be helpful to you.*

__Server side (Linux server):__

1. Install samba: sudo apt-get update && sudo apt-get install samba
2. Create samba account to access share:
    ```
    sudo userdd smbuser
    sudo smbpasswd -a smbuser
    ```
3. Create dir to be shared (adjust this for your user account - 'wlanpi' usr account used in this example)
    ```
    sudo mkdir /home/wlanpi/share
    sudo chown wlanpi:wlanpi /home/wlanpi/share
    ```
4. Edit smb.conf to add share:
    ```
    sudo nano /etc/samba/smb.conf

    # Add this to end of smb.conf - adjust path for your instance
    [shared]
    path = /home/wlanpi/share
    available = yes
    valid users = smbuser
    read only = no
    create mask = 0755
    browsable = yes
    public = yes
    writable = yes
    ```
5. Restart samba: 
    ```
    systemctl restart smbd
    systemctl status smbd
    # make sure our firewall doesn't get in the way (if installed)
    # ** do not leave firewall disabled!!! **
    ufw disable
    ```
__Client side (WLAN Pi/RPi):__

1. Install cifs-utils: : sudo apt-get update && sudo apt-get install cifs-utils

2. Create local mount point:
    ```
    mkdir /tmp/share
    ```
3. Mount the remote volume - adjust IP address for your remote server(s):
    ```
    /sbin/mount.cifs //192.168.0.52/shared /tmp/share -o user=smbuser,pass='smbuser'
    /sbin/mount.cifs //192.168.0.193/shared /tmp/share -o user=smbuser,pass='smbuser'
    ```
4. Copy a file from the remote mount:
    ```
    /bin/cp -f /tmp/share/file.txt ~/.
    ```
5. Unmount volume:
    ```
    /bin/umount /tmp/share
    ```
