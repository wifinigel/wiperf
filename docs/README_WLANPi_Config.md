# Wiperf - Configuration on the WLANPi

This instruction paper assumes you are running Wiperf on a WLANPi on an image verison of v1.9 or later (which has Wiperf installed and available as part of the image.)

The Wiperf probe is activated via the front panel menu system (FPMS) of the WLANPi. But, before flipping in to the Wiperf mode, a few configuration steps need to be completed:

# Configuration File (config.ini)

The operation of Wiperf is configured using the file `'/home/wanpi/wiperf/config.ini'` This needs to be edited prior to entering Wiperf mode.

Prior to the first use of Wiperf, the config.ini file does not exist in the required WLANPi directory. However, a default template config file (`config.default.ini`) is supplied that can be used to create the `config.ini` file. Here is the suggested workflow:

Connect to the WLANPi, create a copy of the config template file and edit the newly created config (as the wlanpi user):

```
        cd /home/wlanpi/wiperf
        cp ./config.default.ini ./config.ini
        nano ./config.ini
```

By default, the configuration file is set to run all tests. However, there is a minimum configuration that must be applied for Wiperf mode to run out-of-the-box. Here are the minimum configuration parameters you need to configure (just to get you going...):

```
[General]
; interface name over which mgt traffic is sent (i.e. how we get to Splunk) - options: wlan0, eth0, zt
mgt_if: wlan0

; Splunk host IP/name
data_host: 192.168.0.99

; Splunk token to access Splunk server created by Splunk (example token: 84adb9ca-071c-48ad-8aa1-b1903c60310d)
splunk_token: 84adb9ca-071c-48ad-8aa1-b1903c60310d

[Iperf3_tcp_test]
; IP address of iperf3 server
server_hostname: 192.168.0.14

; IP address of iperf3 server
server_hostname: 192.168.0.14
```

For a full description of the configuration file parameters, please review the following page: [config.ini reference guide](README_Config.ini.md). The Splunk token is obtained from your Splunk server (see [Splunk build guide][splunk_build]). 

# Wireless Client Configuration (wpa_supplicant.conf)

When the WLANPi is flipped in to Wiperf mode, it will need to join the SSID under test to run the configured tests. We need to provide a configuration (that is only used in Wiperf mode) to allow the WLANPi to join a WLAN.

Edit the following file with the configuration and credentials that will be used by the WLANPi to join the SSID under test once it is switched in to Wiperf mode (make edits logged in as the wlanpi user):

```
        cd /home/wlanpi/wiperf/etc/wpa_supplicant
        nano ./wpa_supplicant.conf
```

# Testing

Once the required edits have been made to configure Wiperf mode, flip the WLANPi in to Wiperf mode using the following FPMS options:

```
        Actions > Wiperf > Confirm
```

If no errors are observed on the FPMS during flip-over, inspect the following files to double-check for errors & verify that test data is generated (as indicated in the log messages):
```    
    cat /home/wlanpi/wiperf/logs/agent.log
    cat /home/wlanpi/wiperf/wiperf.log 
```
Note that by default the tests are run every 5 mins unless the interval has been changed in the `config.ini` file. Wait at least this interval before determining that there is an issue - the test cycle will NOT begin immediately upon entering Wiperf mode.

Check your instance of Splunk and verify that data is being received.

# Updating

To get the latest updates from the GitHub repo (when available), use the following commands when logged in as the wlanpi user:

```
        cd ~/wiperf
        git pull https://github.com/wifinigel/wiperf.git
```

(note that this will update config.default.ini but not config.ini, so remember to re-edit it after a pull if the config file format changes)

# Troubleshooting:

If things seem to be going wrong, try the following:

- Connect to the WLANPi using the USB OTG connection to check log files: 
    - `cat /home/wlanpi/wiperf/logs/agent.log`
    - `cat /home/wlanpi/wiperf/wiperf.log`
- SSH to the device & tail the agent log file in real-time, watching for errors and dumps of test results being performed:`tail -f /home/wlanpi/wiperf/logs/agent.log`
- Flip back in to classic mode and activate Wiperf mode from the CLI of the WLANPi, watching for errors:
    - `cd /home/wlanpi/wiperf`
    - `sudo ./wiperf_switcher`
- Try disabling tests & see if one specific test is causing an issue
- Make sure all pre-reqs have definitely been fulfilled
- Make sure your WLANPi and Splunk servers are NTP sync'ed
- Flip back to classic mode and re-check the edits made to the `config.ini` & `wpa_supplicant.conf` files

# Known Issue:

There seems to be an issue with the Comfast CF-912 adapter when using it with the WLANPi and associating as a client to SSIDs that use 80MHz width channels. If you hit an issue where the WLANPi seems to lock up or does not boot correctly, try a different adapter or a network that does not use 8Mhz channels.

<!-- link list -->
[wlanpi_build]: docs/README_WLANPi_Image_Build.md
[wlanpi_config]: docs/README_WLANPi_Config.md
[config_ini]: docs/README_Config.ini.md
[splunk_build]: https://github.com/wifinigel/wiperf/raw/master/docs/WLANPi%20Wiperf%20Probe%20-%20Splunk%20Build.pdf