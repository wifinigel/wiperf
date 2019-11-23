# wiperf

Wi-Fi performance probe

## Pre-requisites

Update existing Linux packages:

- sudo apt-get update
- sudo apt-get upgrade

Install required Linux packages:

- sudo apt-get install python3-pip
- sudo apt-get install iperf3
- sudo apt-get install git

Install required python3 modules

- sudo pip3 install iperf3
- sudo pip3 install speedtest-cli
- sudo pip3 install configparser

Create the wlanpi user:

- sudo adduser wlanpi

Edit the sudoers file to enable the wlanpi user to run some commands that require elevated privilege:

- sudo visudo
- Add following line to bottom of file: wlanpi  ALL=(ALL) NOPASSWD: ALL

Reboot and log back in with the wlanpi user:

- sudo reboot

With the RPi connected to the Internet, clone this project:

- git clone https://github.com/wifinigel/wiperf.git

Edit the config file to customize the operation of the script:

- nano /home/wlanpi/wiperf/config.ini

Create a cronjob to run the script very 5 mins:

- crontab -e
- add line: 1-59/5 * * * * sudo /usr/bin/python3 /home/wlanpi/wiperf/wi-perf.py > /home/wlanpi/wiperf/wiperf.log 2>&1
  