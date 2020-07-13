Title: Influx Configuration
Authors: Nigel Bowden

# Influx Configuration
<div style="float: right;">![influx_logo](images/influx_logo.png)</div>Now that we have the InfluxDB software installed, the next step is to create a database in which data from our wiperf probes will be stored.

To create the database, we need to execute a series of commands on the CLI of the Influx DB server. Follow the following steps to create the required database:

- Check the InfluxDB service is running before starting ```sudo systemctl status influxdb``` (ensure the process is "active (running)" )
- Enter the InfluxDB shell using the following command: ```sudo influx``` (shell is indicated by the new ">" prompt)
    - Create an admin user to administer InfluxDB:
        - ```CREATE USER admin WITH PASSWORD 'letmein' WITH ALL PRIVILEGES```
- Exit the InfluxDB shell with the command ```exit``` to return to the standard Linux CLI
- Edit the InfluxDB configuration file (/etc/influxdb/influxdb.conf):
    - ```sudo nano /etc/influxdb/influxdb.conf```
    - uncomment the line ```# auth-enabled = false``` in the ```[http]``` section and change to ```auth-enabled = true``` to enable authentication of access to the database
    - restart the InfluxDB process for the change to take effect: ```sudo systemctl restart influxdb```
- Enter the InfluxDB shell again using the following command: ```sudo influx -username admin -password letmein``` (now using authentication)
    - Create a new database with the following commands:
        - ```CREATE DATABASE wiperf```
        - Check the new database exists using: ```SHOW DATABASES``` (the database "wiperf" should be shown in the list)
    - Create and assign a user who can write to the wiperf database (i.e. a probe) using the following CLI commands (note the single and double quotes are signifcant for the user & pwd fields):
        - ```CREATE USER "wiperf_probe" WITH PASSWORD 's3cr3tpwd99'```
        - ```GRANT WRITE ON "wiperf" TO "wiperf_probe"```
    - Create and assign a user who can read from the wiperf database (i.e. the Grafana program) using the following CLI commands (note the single and double quotes are signifcant for the user & pwd fields):
        - ```CREATE USER "grafana" WITH PASSWORD 'R34dth3DB'```
        - ```GRANT read ON "wiperf" TO "grafana"```
- Exit the InfluxDB shell with the command ```exit``` t return to the Linux CLI

At this point, the InfluxDB service is ready to receive data from a probe. If you have any probes ready to go, make sure they use the "wiperf_probe" user credentials in their configuration file so that they can add their data to the database.

If you believe you have a probe that has successfully sent data, you can check the database contents using the following commands in the InfluxDB shell:

 - ```USE wiperf```
 - ```SHOW SERIES```
 - ```SELECT * FROM "wiperf-speedtest"```
 - ```SHOW FIELD KEYS ON "wiperf" FROM "wiperf-speedtest"```

To find out more details, please checkout the official getting started guide: [https://docs.influxdata.com/influxdb/v1.8/introduction/get-started/](https://docs.influxdata.com/influxdb/v1.8/introduction/get-started/){target=_blank}

For more information about adding users, check out: [https://docs.influxdata.com/influxdb/v1.8/administration/authentication_and_authorization/](https://docs.influxdata.com/influxdb/v1.8/administration/authentication_and_authorization/#user-management-commands){target=_blank}


__Note:__ *You are advised to use your own passwords for the password fields shown in this document to ensure they are secured.*