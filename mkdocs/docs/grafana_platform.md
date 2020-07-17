Title: Grafana Platform
Authors: Nigel Bowden

# Grafana Platform
<div style="float: right;">
![grafana_logo](images/grafana_logo.png)
</div>Grafana is an open-source visualization tool that allows us to create reports around the data sent from wiperf probes to InfluxDB. It can integrates with a variety of data sources to query raw data and provides a wide variety of graphical report options - in our case, Grafana integrates with InfluxDB

This guide does not cover all installation details of the software package, as these may be obtained from the official Grafana web site: [https://grafana.com/docs/grafana/latest/](https://grafana.com/docs/grafana/latest/){target=_blank}. Installation instructions are available for all major operating systems. Note that although Windows is supported, if you intend to install Grafana on the same platform as InfuxDB, Windows is not an option as InfluxDB v1.8 does not support Windows. 

To install Grafana and use it with a handful of probes, a modest server may be built (e.g. I use a low-end Intel NUC running Ubuntu), so for testing purposes, don’t get too hung up on sourcing a high end server. If you'd like to look into server requirements further, then [check out this page](https://grafana.com/docs/grafana/latest/installation/requirements/){target=_blank}.

Note that Grafana is an open-source product. There is no cost for downloading and installing your own instance of the software.



