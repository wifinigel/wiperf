
# Troubleshooting:

If things seem to be going wrong, try the following:

- Connect to the WLAN Pi using the USB OTG connection to check log files: 
    - `cat /home/wlanpi/wiperf/logs/agent.log`
    - `cat /home/wlanpi/wiperf/wiperf.log`
- SSH to the device & tail the agent log file in real-time, watching for errors and dumps of test results being performed:`tail -f /home/wlanpi/wiperf/logs/agent.log`
- Flip back in to classic mode and activate Wiperf mode from the CLI of the WLAN Pi, watching for errors:
    - `cd /home/wlanpi/wiperf`
    - `sudo ./wiperf_switcher`
- Try disabling tests & see if one specific test is causing an issue
- Make sure all pre-reqs have definitely been fulfilled
- Make sure your WLAN Pi and Splunk servers are NTP sync'ed
- Flip back to classic mode and re-check the edits made to the `config.ini` & `wpa_supplicant.conf` files
- If you have changed the WLAN Pi hostname from its default, make sure you have updated both the `/etc/hosts` **AND** the `/etc/hostname` file as per the instructions [here][hostname_faq] (this can cause some very weird issues!)
- Check the order of DNS servers being used by running the command `cat /etc/resolv.conf` on the CLI of the WLAN Pi when it is in wiperf mode and connected to the wireless network. If there are multiple servers shown and you see `8.8.8.8` at the top of the list, you may need to move the 8.8.8.8 entry from the file `/etc/resolvconf/resolv.conf.d/head` to `/etc/resolvconf/resolv.conf.d/tail` and then reboot. This should shift 8.8.8.8 to be bottom of the list in `cat /etc/resolv.conf` and may fix your name resolution issues

