Title: Probe Software Upgrade
Authors: Nigel Bowden

# Probe Software Upgrade
Periodically, new versions of wiperf code may be available to add bug-fixes and new features. The wiperf code must be upgraded from the CLI of the probe.

For the WLAN Pi, it is generally recommend to use the version shipped with the WLAN Pi image, but there may be instances when there is a need to upgrade the wiperf code (e.g. in the case of a bug) before the next WLAN Pi image upgrade. The instructions for each probe type are provided below.

Instructions are also provided for upgrading to the latest 'dev' release. This code will generally be "bleeding edge", so it's best to avoid this option unless directed by the code developers. 

## WLAN Pi

### Upgrade To Latest Stable Release
Execute the following commands on the WLAN Pi CLI:

```
# check the curent installed version and latest available version:
sudo /usr/share/wiperf/setup.sh check_ver
```

```
# perform the upgrade (probe must be connected to Internet)
curl -s https://raw.githubusercontent.com/wifinigel/wiperf/main/setup.sh | sudo bash -s upgrade wlanpi
```

### Upgrade To Latest Dev Release
Execute the following commands on the WLAN Pi CLI:

```
# perform the upgrade (probe must be connected to Internet)
curl -s https://raw.githubusercontent.com/wifinigel/wiperf/dev/setup.sh | sudo bash -s upgrade wlanpi
```

## Raspberry Pi

### Upgrade To Latest Stable Release
Execute the following commands on the RPi CLI:

```
# check the curent installed version and latest available version:
sudo /usr/share/wiperf/setup.sh check_ver
```

```
# perform the upgrade (probe must be connected to Internet)
curl -s https://raw.githubusercontent.com/wifinigel/wiperf/main/setup.sh | sudo bash -s upgrade rpi
```

### Upgrade To Latest Dev Release
Execute the following commands on the RPi CLI:

```
# perform the upgrade (probe must be connected to Internet)
curl -s https://raw.githubusercontent.com/wifinigel/wiperf/dev/setup.sh | sudo bash -s upgrade rpi
```