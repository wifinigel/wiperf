Title: Influx Installation
Authors: Nigel Bowden

# Influx Installation
Obtaining and installing the InfluxDB software is very straightforward. The following steps provide a high level over view of the steps required:

- Visit the InfluxDB v1.8 installation guide at [https://docs.influxdata.com/influxdb/v1.8/introduction/install/](https://docs.influxdata.com/influxdb/v1.8/introduction/install/)
- Scroll down to the "Installing InfluxDB OSS" section
- Select the OS of the platform that you will be using to host your instance of InfluxDB
- Copy the commands provided for your server OS to add the required software repository
- SSH to the server that will be used to host InfluxDB
- Paste in the commands copied from the installation page on to the CLI of your server. These will ensure your server can find the required repository to pull the InfluxDB software
- To get the required commands to download & install the software, visit the following web page and select the v1.8 download option: [https://portal.influxdata.com/downloads/](https://portal.influxdata.com/downloads/)
- Copy the install commands provided for your OS
- Make sure your server has Internet connectivity (as it will need to pull down the required software)
- On the CLI of your server, paste in the copied commands to kick-off the software download & install
- Once installation is complete, start the InfluxDB processes with the server CLI command: ```sudo systemctl start influxdb```
- Check the software is installed and running by executing the following command on the server CLI: ```sudo systemctl status influxdb``` (ensure the process is "active (running)" )


The next step is to create a database to drop our incoming data (from wiperf probes) into.

