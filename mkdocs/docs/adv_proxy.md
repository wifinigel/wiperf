Title: Proxy Server
Authors: Nigel Bowden

# Proxy Server
If you need to deal with using a proxy on your network, please supply the details of your proxy by completing the following section in your ```/etc/wiperf/config.ini``` file:

```
; If proxy server access is required to run a speedtest, enter the proxy server details here for https & https
; e.g. https_proxy: http://10.1.1.1:8080
;
; For sites that are not accessed via proxy, use no_proxy (make sure value enclosed in quotes & comma separated for mutiple values)
; e.g. no_proxy: "mail.local, intranet.local"
http_proxy: 
https_proxy:
no_proxy:
```
