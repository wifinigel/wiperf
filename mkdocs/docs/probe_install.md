Title: Probe Software Installation
Authors: Nigel Bowden

# Probe Software Installation
This section takes a look at how we install various additional required software packages on to our probe. This includes any pre-requisite software packages and the wiperf software itself.

## WLAN Pi
Good news! If you're using a WLAN Pi (v2.x image), you already have the software required (it's part of the WLAN Pi software image). Go to the [next section of this documentation site](probe_configure.md).

!!! Note
    __New in V2.1:__ For SMB test support or to use Librespeed for speedtest, you will need to install a couple of optional extra packages as detailed in these reference documents:

    * [SMB test Support](reference_doc_smb.md)
    * [Librespeed Support](reference_doc_librespeed.md)

## Raspberry Pi
The RPi requires a few pre-requisite Linux packages before we can install the wiperf software itself. Note that the probe must be connected to a network (via ethernet or wireless) that has access to the Internet to download the required code.

You will need CLI access to the probe to perform the steps detailed below.

### Package Updates
Before we start adding pre-requisite packages, it's always a good idea to update the existing Linux packages on our RPi to make sure we have the "latest and greatest". This may take a few minutes to complete as many files may be downloaded & updated, depending on when/if your RPi was last updated:

```
# download & update latest Linux packages
sudo apt-get update && sudo apt-get upgrade -y
# Reboot if any new packages were installed
sudo reboot
```

### Pre-requisite Packages
Next, we need to install additional Linux packages that may not be included as part of the standard RPi distribution: 

- pip3
- iperf3
- git 
- curl
- netcat

These are installed with the following CLI commands:

```
sudo apt-get update
sudo apt-get install python3-pip iperf3 git curl netcat -y
sudo reboot
```

!!! Note
    __New in V2.1:__ For SMB test support or to use Librespeed for speedtest, you will need to install a couple of optional extra packages as detailed in these reference documents:

    * [SMB test Support](reference_doc_smb.md)
    * [Librespeed Support](reference_doc_librespeed.md)

### wiperf Software Installation
To install the wiperf code itself on to the RPi, execute the following CLI command:

```
curl -s https://raw.githubusercontent.com/wifinigel/wiperf/main/setup.sh | sudo bash -s install rpi
```

This will initiate the download and installation of a number of python packages, together with the wiperf code itself. This will take a few minutes to complete.


Once installation is complete, our final step is to [configure the wiperf probe](probe_configure.md) to perform the tests we'd like to run, and provide details of where the probe needs to send its data (i.e. our data server).
     
