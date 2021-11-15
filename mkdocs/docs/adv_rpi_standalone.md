Title: RPi Standalone Probe With Reporting
Authors: Nigel Bowden

# RPi Standalone Probe With Reporting

## Overview 

The wiperf project is primarily concerned with the functionality of the SBC network UX probe function The probe performs a variety of network tests to provide an indication of user network experience. 

The wiperf probe is generally deployed as a standalone probe, running regular network tests and exporting results data to either a Splunk or InfluxDB/Grafana reporting server. The remote reporting server is used to perform data analysis and reporting..

However, there may be instances when it may be useful to run the probe with both the network testing and reporting features on the probe. This option is not available when using Splunkas the reporting server, as it cannot run its server software on the RPi. However, testing has shown that InfluxDB and Grafana can be successfully installed on to an RPi so that the probe and reporting features can co-exist on one device. In this configuration, the wiperf probe function sends its results data to  InfluxDB and Grafana installed on the same physical RPi.

This has been tested with an RPi 3B+, but will likely be fine with all subsequent models of RPi. 

__Note__: It is not recommended to install Grafana and InfluxDB on to an RPi to act as a centralised server for multiple probes - a higher power dedicated server is advised to support data from multiple probes. However, combined testing and reporting for a local probe on the same RPi seems to work OK based on initial testing. One caveat is that it is likely worth setting a data retention policy as outlined below to ensure the InfluxDB does not consume too much space on the RPi as data is gathered over time.

__Note:__ The steps outlined below are notes taken from initial testing. This is an advanced level topic that requires that you are familiar with Linux commands and the operation of wiperf. Apologies that the information provided is relatively concise, but this is an advanced level configuration. 

## What You'll Need

In this article, I'll run through the build process to get all all-in-one wiperf probe built (wiperf + InfluxDB + Grafana on the same RPi). To perform this build, you'll need:

- A Raspberry Pi (3B+ or 4 is probably the best choice as they have internal wireless NIC)
- A 16Gb or better Micro SD card
- A power source/adapter for the Rpi
- A USB to micro-SD adapter to burn the image (for example: [an adapter like this](https://www.amazon.com/Vanja-Adapter-Portable-Memory-Reader/dp/B00W02VHM6){target=_blank}
- A copy of [balenaEtcher](https://www.balena.io/etcher/){target_blank} (free) to burn the image on to your SD card

You'll need to burn a fresh image by downloading a copy of the latest [Raspberry Pi OS](https://www.raspberrypi.org/software/operating-systems/). I'd advise using the 'Lite' version of the image, as this is a simple, headless probe device (and that is what I have tested). Use [balenaEtcher](https://www.balena.io/etcher/){target_blank} to burn the image on to your micro-SD card. Put it in to the SD slot of the RPi and boot it. You can find more extensive [instructions here](probe_prepare.md#raspberry-pi) about building and accessing the RPi to use as a wiperf probe - the focus of this document is the all-in-one software build.

## Setup Procedure

__All of the steps below are performed from the RPi CLI (this guide assumes you are running Raspbian Buster and that you have remote access to the RPI, with all networking configured and ready to go (if not, [see here](probe_prepare.md#raspberry-pi) )):__

1.Update RPi packages and reboot (unless already done as part of the probe build process).

```
sudo apt update
sudo apt upgrade
sudo reboot
```

2.Install wiperf:

```
curl -s https://raw.githubusercontent.com/wifinigel/wiperf/main/setup.sh | sudo bash -s install rpi
sudo cp /etc/wiperf/config.default.ini /etc/wiperf/config.ini
```

3.Add a cron job as show below:

```
line="0-59/5 * * * * /usr/bin/python3 /usr/share/wiperf/wiperf_run.py > /var/log/wiperf_cron.log 2>&1"
USERNAME=root  
(sudo crontab -u $USERNAME -l; echo "$line" ) | sudo crontab -u $USERNAME -
```

4.Add the required InfluxDB key & repo details:

```
sudo wget -qO- https://repos.influxdata.com/influxdb.key | sudo apt-key add -
echo "deb https://repos.influxdata.com/debian buster stable" | sudo tee /etc/apt/sources.list.d/influxdb.list
sudo apt update
sudo apt install influxdb
```

5.Once installed, start up InfluxDB & set InfluxDB to start-up on boot

```
sudo systemctl unmask influxdb
sudo systemctl enable influxdb
sudo systemctl start influxdb
```

6.Add pre-requisite packages for Grafana, get & install the Grafana package:

```
sudo apt-get install -y adduser libfontconfig1
wget https://dl.grafana.com/oss/release/grafana-rpi_6.7.4_armhf.deb
sudo dpkg -i grafana-rpi_6.7.4_armhf.deb
```

7.Once Grafana installed, set it to startup on boot & start the Grafana process:

```
sudo systemctl enable grafana-server
sudo systemctl start grafana-server
```

8.On the RPI CLI, prepare Influx DB for data using Influx CLI client (you may want to set your own credentials here!):

```
influx
create database wiperf
create retention policy "wiperf_30_days" on "wiperf" duration 30d replication 1
CREATE USER admin WITH PASSWORD 'letmein' WITH ALL PRIVILEGES
exit
```

9.Edit InfluxDB to use login authentication & restart its processes to activate the change:

```
sudo nano /etc/influxdb/influxdb.conf (uncomment "# auth-enabled = false" -> "auth-enabled = true")
sudo systemctl restart influxdb
```

10.On RPI CLI, drop in to the Influx CLI client again and create some credentials for the probe login (you may want to set your own credentials here!)

```
influx -username admin -password letmein
CREATE USER "wiperf_probe" WITH PASSWORD 's3cr3tpwd99'
GRANT WRITE ON "wiperf" TO "wiperf_probe"
CREATE USER "grafana" WITH PASSWORD 'R34dth3DB'
GRANT read ON "wiperf" TO "grafana"
exit
```

11.Edit the wiperf configuration file to use the loopback interface as the management interface and set the InfluxDB details (use the probe credentials you created for InfluxDB)

```
sudo nano /etc/wiperf/config.ini
mgt_if: lo
exporter_type: influxdb
influx_host: 127.0.0.1
influx_port: 8086
influx_username: wiperf_probe
influx_password: s3cr3tpwd99
influx_database: wiperf
```

12.Grafana GUI (these steps are completed using a browser):

    Browser: http:<ip>:3000 (login admin/admin, changed on first login)

    In web GUI, add datasource: Configuration > Datasources

    - Type: InfluxDB
    - Name: WiperfDB
    - URL: http://127.0.0.1:8086
    - Access: Server
    - Database: wiperf
    - User: grafana
    - Password: R34dth3DB
    - HTTP Method: GET

13.Obtain the Grafana dashboard files from the wiperf dashboards folder and place on your browser machine (/usr/share/wiperf/dashboards)

    Using the web GUI, import dashboards using these menu options: 

        "+" > Create > Import > Upload .json file > select dashboard file 

        Select folder (General by default)
        Select WiperfDB
    
    Repeat for each dashboard required.

At this point, you should be good to go! Verify the status of polling using the usual wiperf log file (runs every 5 minutes):

```
tail -f /var/log/wiperf_agent.log
```