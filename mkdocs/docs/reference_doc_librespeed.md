Title: Librespeed Speedtest
Authors: Nigel Bowden

# Librespeed Speedtest

!!! Note
    __New in V2.1__

!!! Attention
    Make sure you checkout the ["Known Issues"](#known-issues) section at the end of this page

In addition to performing a speedtest using the public Ookla service, it is now possible to add support for performing speedtesting to [Librespeed](https://librespeed.org/) servers. 

One useful point to note is that in addition to testing against public Librespeed servers,it is also possible to test against your own instance of the Librespeed server. This allows testing within your own environment, without hitting the Internet (and associated bottlenecks)

Switching between using Ookla and Librespeed is achieved by modifying the `provider` parameter in the [Speedtest] section of config.ini:

```
; ====================================================================
;  Speedtest test settings
;  (Changes made in this section will be used in next test cycle
;   and may be made while in Wiperf mode on the WLANPi)
; ====================================================================
[Speedtest]
; yes = enabled, no = disabled
enabled: yes
;
; Speedtest provider valid options: ookla or librespeed
provider: librespeed
; 
; Ookla:
; The server ID of a specific Ookla server taken from : https://c.speedtest.net/speedtest-servers-static.php
; Note this must be the number (NOT url!) taken from the field id="xxxxx". If not specified, best server used (default)
;
; Librespeed:
; The numeric server ID of the server listed in the avaiable servers seen by running the Librespeed CLI
; command: librespeed-cli --list
;
server_id: 
;
; Additional args to pass to Librespeed CLI command (e.g. --local-json /etc/wipef/localserver.json --duration 20) - Note: Librespeed only
librespeed_args: 
;
; If proxy server access is required to run a speedtest, enter the proxy server details here for https & https
; e.g. https_proxy: http://10.1.1.1:8080
;
; For sites that are not accessed via proxy, use no_proxy (make sure value enclosed in quotes & comma separated for mutiple values)
; e.g. no_proxy: "mail.local, intranet.local"
http_proxy: 
https_proxy:
no_proxy:
;
; ------------- Advanced settings for Speedtest section, do not change --------------
; Name used for speedtest file/data group/data source
speedtest_data_file: wiperf-speedtest
;------------------------------ Speedtest Section End -------------------------------
```

In addition to choosing the speedtest provider, it is also possible to choose the specific server ID that is to be used for testing, together with the option of passing additional arguments to the Librespeed test client to control its behaviour. See the inline comments in the config file extract above for more details.

## Pre-requisites - Librespeed Client
The Librespeed speedtest is performed by using the client available from the client GitHub site: [client binaries](https://github.com/librespeed/speedtest-cli/releases){target=_blank}

The Librespeed client is not installed by default on the WLAN Pi or RPi, so must be downloaded and installed before it can be selected as an option for use by wiperf. To install the client, you will need to SSH to the probe and perform the following steps on the CLI:

### RPi
To download and install the Librespeed client on the Raspberry Pi, follow these instructions:

```
# RPi librespeed install
# go to your home dir
cd ~

# get the librespeed-cli binary for RPi
wget https://github.com/librespeed/speedtest-cli/releases/download/v1.0.7/librespeed-cli_1.0.7_linux_armv7.tar.gz

# extract the files
tar xvzf librespeed-cli_1.0.7_linux_armv7.tar.gz

# change the owner of the cli utility to root
sudo chown root:root librespeed-cli

# copy the cli utility to its final destination
sudo cp ./librespeed-cli /usr/local/bin/

# verify librespeed cli is ready to go
librespeed-cli --version
```

### WLAN Pi
To download and install the Librespeed client on the WLAN Pi, follow these instructions:

```
# WLAN Pi librespeed install
# go to your home dir
cd ~

# get the librespeed-cli binary for RPi
wget https://github.com/librespeed/speedtest-cli/releases/download/v1.0.7/librespeed-cli_1.0.7_linux_arm64.tar.gz

# extract the files
tar xvzf librespeed-cli_1.0.7_linux_arm64.tar.gz

# change the owner of the cli utility to root
sudo chown root:root librespeed-cli

# copy the cli utility to its final destination
sudo cp ./librespeed-cli /usr/local/bin/

# verify librespeed cli is ready to go
librespeed-cli --version
```

## Known Issues

There is a known issue on some platforms where librespeed will not run without specifying a specific server ID - this seems to be an issue with ping in Go (the language the client is written in). (*This has been seen on the WLAN Pi*)

To see a list of servers to pick an ID to test against, run the following command to get a list of available servers:

```
librespeed-cli --list
```
Enter the chosen server numeric ID in the `server_id:` field of config.ini