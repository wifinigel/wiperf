Title: Probe Summary
Authors: Nigel Bowden

# Dashboard - 01 - Probe Summary

## Overview
The probe summary report attempts to provide a high level view of the tests that are run by the probe. By providing summary data in one place, it allows view of correlation between any factors that may be causing performance issues.

For instance, if HTTP tests are showing a drop in response times, by looking at other test results, it is possible to see if this issue is limited to just HTTP traffic or maybe other network conditions are the root cause of the issue. If a low physical connection rate on the wireless connection is also observed, the the issue is more likely to be related to a wireless connection issue than a connectivity elsewhere on the network, such as an overloaded Internet WAN link.

By observing the results of all tests, an assessment of the likely fault domain is more readily available by inspecting this report.

## Grafana
For an overview of this report please see [this explanation](#overview)

### Report Panels

#### Speedtest (Download/Upload) 
This panel show the results of tests to the Ookla speedtest service. The average upload and download speeds (in mbps) are shown.

Note that although these results are interesting, they are results from servers that are out on the Internet. The results are going to be subject to the varying conditions on those servers, the Internet network infrastructure itself and your own organizations's Internet pipe. These factors are likely to vary significantly during the day as conditions change.  

Unless there are other supporting test results, poor speedtest results should not be taken as a definitive indication of an issue on your infrastructure. These results are useful when correlated with other network test results, but their value in isolation is limited.

#### Wireless Connection Rate/Signal 
TBA

#### DNS Lookup Time (mS)
TBA

#### HTTP Server Response Time (mS)
TBA

#### DHCP Renewal Time 
TBA

#### TCP iPerf Rate
TBA

#### Ping Targets RTT Avg Times
TBA

#### UDP iPerf Throughput
TBA

#### iPerf UDP (Jitter/Loss)
TBA

#### Poller Status Info
TBA



## Splunk
For an overview of this report please see [this explanation](#overview) 

### Report Panels

#### Speedtest (Download/Upload) 
This panel show the results of tests to the Ookla speedtest service. The average upload and download speeds (in mbps) are shown.

Note that although these results are interesting, they are results from servers that are out on the Internet. The results are going to be subject to the varying conditions on those servers, the Internet network infrastructure itself and your own organizations's Internet pipe. These factors are likely to vary significantly during the day as conditions change.  

Unless there are other supporting test results, poor speedtest results should not be taken as a definitive indication of an issue on your infrastructure. These results are useful when correlated with other network test results, but their value in isolation is limited.

#### Wireless Connection Rate/Signal 
TBA

#### DNS Lookup Time (mS)
TBA

#### HTTP Server Response Time (mS)
TBA

#### DHCP Renewal Time 
TBA

#### TCP iPerf Rate
TBA

#### Ping Targets RTT Avg Times
TBA

#### UDP iPerf Throughput
TBA

#### iPerf UDP (Jitter/Loss)
TBA

#### Poller Status Info
TBA
