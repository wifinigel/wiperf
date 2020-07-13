Title: Probe Deployment
Authors: Nigel Bowden

# Probe Deployment
Once the probe is configured and tested, it's time to deploy it out in the real world.

When deploying, here are a few things to check and remember:

1. Verify that the probe has the network connectivity that you expect once it has been deployed. The following CLI commands will help to check connectivity:
    1. Wireless NIC: ```iwconfig``` (is the probe joining the wireless network?)
    2. IP address: ```ifconfig``` (do the interfaces being used have an IP address?)
    3. Internet connectivity: ```ping google.com``` (can the probe get to the Internet, if that is expected?)
2. Is the probe deployed in the topology you originally intended? If the environment is not as you expected and you need to use a different interface for a particular operation, make sure you have updated ```config.ini``` so that wiperf knows where to send traffic (otherwise, you may hit routing issues)
3. Check the output of ```/var/log/wiperf_agent.log``` to make sure everything is working with no issues once deployed. If there are hitches, they will generally be highlighted in this file, with a detailed explanation of what has failed. 

If you run in to any deployment issues, check out the [troubleshooting](troubleshooting.md) and [FAQ](faq.md) sections of this site.




