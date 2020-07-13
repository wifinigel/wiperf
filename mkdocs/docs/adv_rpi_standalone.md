Title: RPi Standalone Probe With Reporting
Authors: Nigel Bowden

# RPi Standalone Probe With Reporting
The wiperf project is primarily concerned with the functionality of the probe function that performs network tests to give an indication of the user network experience. It provides data to either Splunk or InfluxDB/Grafana that then provide the reporting function.

It is generally recommended that the probe be deployed with a centrally located, remote, reporting server.

However, it may be useful to run the probe as a standalone device with the reporting features also installed on the probe. This cannot be done with Splunk, as it cannot run its server software on the RPi. Testing has shown that InfluxDB and Grafana can be successfully installed on to an RPi so that the probe and reporting features can co-exist on one device.

This has been tested with an RPi 3B+, but will likely be fine with all subsequent models of RPi. It is not recommended to install Grafana and InfluxDB on to an RPi to act as a centralised server for multiple probes, but providing reporting for a local probe on the same RPi seems to work OK based on initial testing. The only caveat is that I would recommend setting a data retention policy as outlined below to ensure the InfluxDB does not consume too much space on the RPi as data is gathered over time.

__Note:__ The steps outlined below are notes taken from initial testing. This is an advanced level topic that requires that you are familiar with Linux commands and the operation of wiperf. Apologies that there is very concise information provided, but this really is an advanced level topic that I cannot generally provide support for. 

```
#############################
# All steps done on RPi CLI
#############################
# update RPi packages (assumes Raspian Buster)
sudo apt update
sudo apt upgrade
sudo reboot

# Install wiperf:
curl -s https://raw.githubusercontent.com/wifinigel/wiperf/setup.sh | sudo bash -s install rpi
# Add cron job (use entry shown)
sudo crontab -e
# add entry: 0-59/5 * * * * /usr/bin/python3 /usr/share/wiperf/wiperf_run.py > /var/log/wiperf_cron.log 2>&1

# Add InfluxDB key & repo
sudo wget -qO- https://repos.influxdata.com/influxdb.key | sudo apt-key add -
echo "deb https://repos.influxdata.com/debian buster stable" | sudo tee /etc/apt/sources.list.d/influxdb.list
sudo apt update
sudo apt install influxdb

# Once installed, set InfluxDB to start up & start process on boot
sudo systemctl unmask influxdb
sudo systemctl enable influxdb
sudo systemctl start influxdb


# Add pre-reqs for Grafan Grafana, get & install pkg
sudo apt-get install -y adduser libfontconfig1
wget https://dl.grafana.com/oss/release/grafana-rpi_6.7.4_armhf.deb
sudo dpkg -i grafana-rpi_6.7.4_armhf.deb

# Once Grafana installed, set for startup & start process
sudo systemctl enable grafana-server
sudo systemctl start grafana-server

# On RPI CLI, prepare Influx DB for data using Influx CLI client:

influx
> create database wiperf
> create retention policy "wiperf_30_days" on "wiperf" duration 30d replication 1
> CREATE USER admin WITH PASSWORD 'letmein' WITH ALL PRIVILEGES
> exit

# Edit InfluxDB to use login auth & restart processes to activate
sudo nano /etc/influxdb/influxdb.conf (uncomment "# auth-enabled = false" -> "auth-enabled = true")
sudo systemctl restart influxdb

# On RPI CLI, drop in to Influx CLI client again
influx -username admin -password letmein
> CREATE USER "wiperf_probe" WITH PASSWORD 's3cr3tpwd99'
> GRANT WRITE ON "wiperf" TO "wiperf_probe"
> CREATE USER "grafana" WITH PASSWORD 'R34dth3DB'
> GRANT read ON "wiperf" TO "grafana"

# Edit wiperf config file to use local mgt i/f, Influx DB & loging credentials

sudo nano /etc/wiperf/config.ini
mgt_if: lo
exporter_type: influxdb
influx_username: wiperf_probe
influx_password: s3cr3tpwd99
influx_host: 127.0.0.1

# Grafana GUI (these steps done from browser):

Browser: http:<ip>:3000 (login admin/admin, changed on first login)

In web GUI, add datasource: Configuration > Datasources

- Type: InfluxDB
- Name: WiperfDB
- URL: htttp://127.0.0.1:8086
- Access: Server
- Database: wiperf
- User: grafana
- Password: R34dth3DB

Obtain the Grafana dashboard files from the wiperf dashboards folder and place on your browser machine (/usr/share/wiperf/dashboards)
In web GUI, import dashboards: + Create > Import > Upload .json file > select dashboard file 
```

