Title: Influx Installation
Authors: Nigel Bowden

# Influx Installation
<div style="float: right;">![influx_logo](images/influx_logo.png)</div>Obtaining and installing the InfluxDB software is very straightforward. here is a high-level overview of the steps required:

- On your laptop, open a browser and obtain the required commands to download & install the software by visiting the following web page and selecting the v1.8 download option: [https://portal.influxdata.com/downloads/](https://portal.influxdata.com/downloads/){target=_blank}
- Copy the install commands provided for your OS
- Make sure your InfluxDB server has Internet connectivity (as it will need to pull down the required software)
- SSH to the server that will be used to host InfluxDB
- On the CLI of your server (your SSH session), paste in the copied commands to kick-off the software download & install
- Once installation is complete, start the InfluxDB processes with the server CLI command: ```sudo systemctl start influxdb```
- Make sure the InfluxDB service starts after a platform reboot: ```sudo systemctl enable influxdb```
- Check the software is installed and running by executing the following command on the server CLI: ```sudo systemctl status influxdb``` (ensure the process is "active (running)" )

The next step is to [create a database](influx_configure.md) to drop our incoming data (from wiperf probes) into.

