Title: Splunk Installation
Authors: Nigel Bowden

# Splunk Installation
<div style="float: right;">![splunk_logo](images/splunk_logo.png)</div>Once the software is downloaded, follow the instructions that are appropriate for your OS in the Splunk installation manual:

[https://docs.splunk.com/Documentation/Splunk/latest/Installation/Chooseyourplatform](https://docs.splunk.com/Documentation/Splunk/latest/Installation/Chooseyourplatform)

The installation process for all platforms is very straightforward and is detailed in the official install guides, so will not be covered in detail here.

!!! note Debian Linux 

    When installing the Linux flavour of Splunk, make sure you do not miss the additional step required to ensure that Splunk starts after a server reboot. The following command needs to be executred after the software is installed (but please verify this isn the official installation documents):

    ```
        sudo /opt/splunk/bin/splunk enable boot-start
    ```

Once installation has been completed, it should be possible to access the web dashboard of Splunk at the URL:

```
    http://<Splunk_server_IP>:8000
```

![splunk_login](images/splunk_login.png)