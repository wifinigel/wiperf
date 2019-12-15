# Wiperf - Configration on the WLANPi

This instruction paper assumes you are running Wiperf on a WLANPi on an image verison of v1.8.5 or later (which has Wiperf installed and avaiable as part of the image.)

The Wiperf probe is activate via the front panel menu system (FPMS) of the WLANPi. But, before flipping in to the Wiperf mode, a few configuration steps need to be completed:

# Configuration File (config.ini)

The operation of Wiperf is configured using the file '/home/wanpi/wiperf/conig.ini' This needs to be edited prior to entering Wiperf mode.

Prior to the first use of Wiperf, the config.ini file does not exist in the requried WLANPi directory. However, a default template config file (config.default.ini) is supplied that can be used to create the config.ini file. Here is the suggested wokflow:

Connect to the WLANPi, create a copy of the config template file and edit the newly created config (as the wlanpi user):

```
        cd /home/wlanpi/wiperf
        cp ./config.default.ini ./config.ini
        nano ./config.ini
```

When the WLANPi is flipped in to Wiperf mode, it will need to join the SSID under test and run the configured tests. We need to provide a configuration (that is only used in Wiperf mode) to allow the WLANPi to join a WLAN.

Edit the following file with the configuration and credentials that will be used by the WLANPi to join the SSID under test once it is switched in to Wiperf mode (make edits logged in as the wlanpi user):

```
        cd /home/wlanpi/wiperf/etc/wpa_supplicant
        nano ./wpa_supplicant.conf
```

# Testing

Once the required edits have been made to configure Wiperf mode, flip the WLANPi in to Wiperf mode using the following FPMS options:

```
        /usr/bin/python3 /home/wlanpi/wiperf/wi-perf.py
```

If no errors are observed when running it then check the following files to double-check for errors & verify that data is generated (as indicated in the ):
```    
        Actions > Wiperf > Confirm
```

Check your instance of Splunk and verify that data is being received.

# Updating

To get the latest updates from the GitHub repo, use the following commands when logged in as the wlanpi user:

```
        cd ~/wiperf
        git pull https://github.com/wifinigel/wiperf.git
```

(note that this will update config.default.ini but not config.ini, or remember to re-edit it after a pull if the format changes)

# Troubleshooting:

If things seem to be going wrong, try the following:

- Connect to the WLANPi using the USB OTG connection to check log files: 
    - cat /home/wlanpi/wiperf/logs/agent.log
    - cat /home/wlanpi/wiperf/wiperf.log
- Flip back in to classic mode and activate Wiperf mode from the CLI of the WLANPi, watching for errors:
    - cd /home/wlanpi/wiperf
    - sudo ./wiperf_switcher)
- SSH to the device & tail the log files in real-time, wtaching for errors and dumps of test results being performed: tail -f /home/wlanpi/wiperf/logs/agent.log
- Try disabling tests & see if one specific test is causing an issue
- Make sure all pre-reqs have definitely been fulfilled

# Known Issue:

There seems to be an issue with the Comfast CF-912 adapter when using it with the WLANPi and associating as a client to SSIDs that use 80MHz width channels. If you hit an issue where the WLANPi seems to lock up or does not boot correctly, try a different adapter or a network that does not use 8Mhz channels.
  