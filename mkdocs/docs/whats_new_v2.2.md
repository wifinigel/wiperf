Title: What's New in version 2.2
Authors: Nigel Bowden

# What's New in version 2.2
<div style="float: right;">
![wiperf_logo](images/wiperf_logo.png)
</div>
<span style="font-size: small; color:gray">*27th January 2021 - Author: Nigel Bowden*</span><br><br>
Version 2.2 of the wiperf probe code follows hot on the heels of v2.1, following several requests from the community for removal of limitations on the number of test targets for several of the tests performed by wiperf. Previously, the Ping, HTTP, DNS and SMB tests were limited to 5 test targets. In v2.2, these limits are removed and the number of test targets is now user defined.

---

__Note: Please make sure you review the [v2.1 release notes](whats_new_v2.1.md) if you're jumping straight from v2.0 to v2.2__

---

## Ping Tests

The ping tests section of config.ini is now structured as shown below:

```
; ====================================================================
;  Ping tests settings
;  (Changes made in this section will be used in next test cycle
;   and may be made while in Wiperf mode on the WLANPi)
; ====================================================================
[Ping_Test]
; yes = enabled, no = disabled
enabled: yes
;
; Number of targets we'd like to ping
ping_targets_count: 2
; first host we'd like to ping
ping_host1: google.com
;
; second host we'd like to ping
ping_host2: cisco.com
;
; add more ping targets to match your "ping_targets_count" value
; ping_host3: 
; ping_host4:
; ping_host5:
; ping_host6:
;....etc
;
; number of pings to send per test
ping_count: 10
;
; Timeout value for pings (in secs)
ping_timeout: 1
;
; Interval between pings (in secs)
ping_interval: 0.2
;
; ------------ Advanced settings for Ping tests section, do not change -------------
; Name used for ping_test file/data group/data source
ping_data_file: wiperf-ping
;-------------------------------- Ping Section End ---------------------------------
```

Note the new `ping_targets_count` field which allows the number of ping targets to be user-defined. Note that additional `ping_host` entries need to be added to correspond with the number of targets specified.

Also new for v2.2 are the `ping_timeout` and `ping_interval` fields. These allow for the optimization of ping testing and prevent long delays when pinging large numbers, or poorly performing targets. 

## DNS Tests

The number of DNS tests that are performed during a poll cycle may now be user-defined, rather than being limited to 5 test entries. A new field within config.ini : `dns_targets_count` provides the count of the number of tests to be performed.

Additionally, as many `dns_target` entries as required may be added to match up with the number of targets defined. 

See the extract from the new config.ini template file below showing the new options:

```
; ====================================================================
;  DNS tests settings
;  (Changes made in this section will be used in next test cycle
;   and may be made while in Wiperf mode on the WLANPi)
; ====================================================================
[DNS_test]
; yes = enabled, no = disabled
enabled: yes
;
; Number of DNS targets we'd like to test
dns_targets_count: 2
;
; First DNS target
dns_target1: google.com
;
; Second DNS target
dns_target2: cisco.com
;
; add more DNS targets to match your "dns_targets_count" value
; dns_target3: 
; dns_target4:
; dns_target5:
; dns_target6:
;....etc
;
; ------------ Advanced settings for DNS tests section, do not change --------------
; Name used for dns_test file/data group/data source
dns_data_file: wiperf-dns
;-------------------------------- DNS Section End ----------------------------------
```

## HTTP Tests

The number of HTTP tests that are performed during a poll cycle may now be user-defined, rather than being limited to 5 test entries. A new field within config.ini : `http_targets_count` provides the count of the number of tests to be performed.

Additionally, as many `http_target` entries as required may be added to match up with the number of targets defined. 

See the extract from the new config.ini template file below showing the new options:

```
; ====================================================================
;  HTTP tests settings
;  (Changes made in this section will be used in next test cycle
;   and may be made while in Wiperf mode on the WLANPi)
; ====================================================================
[HTTP_test]
; yes = enabled, no = disabled
enabled: yes
;
; Number of HTTP targets we'd like to test
http_targets_count: 2
;
; First HTTP target
http_target1: https://google.com
;
; Second HTTP target
http_target2: https://cisco.com
;
; add more HTTP targets to match your "http_targets_count" value
; http_target3: 
; http_target4:
; http_target5:
; http_target6:
;....etc
;
; -------------- Advanced settings for HTTP tests section, do not change ----------------
; Name used for http_test file/data group/data source
http_data_file: wiperf-http
;-------------------------------- HTTP Section End ---------------------------------
```

## SMB Tests

The number of SMB tests that are performed during a poll cycle may now be user-defined, rather than being limited to 5 test entries. A new field within config.ini : `smb_targets_count` provides the count of the number of tests to be performed.

Additionally, as many SMB entries as required may be added to match up with the number of targets defined. This will require the creation of an `smb_host1`,  
`smb_username`, `smb_password`, `smb_path` and `smb_filename` field for each target (see examples below)

See the extract from the new config.ini template file below showing the new options:

```
; ====================================================================
;  SMB tests settings
;  (Changes made in this section will be used in next test cycle
;   and may be made while in Wiperf mode on the WLANPi)
; ====================================================================
[SMB_test]
; yes = enabled, no = disabled
enabled: no
;
; Number of SMB targets we'd like to test
smb_targets_count: 2
;
; username and password to be used for all tests if all
; tests use same credentials
smb_global_username: 
smb_global_password: 
;
; first host we'd like to test
smb_host1: 
smb_username1: 
smb_password1: 
smb_path1: 
smb_filename1: 
;
; second host we'd like to test
smb_host2: 
smb_username2: 
smb_password2: 
smb_path2: 
smb_filename2: 
;
; add more SMB targets to match your "smb_targets_count" value
;smb_host3: 
;smb_username3: 
;smb_password3: 
;smb_path3: 
;smb_filename3: 
;
;smb_host4: 
;smb_username4: 
;smb_password4: 
;smb_path4: 
;smb_filename4: 
; ...etc
;
; ------------ Advanced settings for SMB tests section, do not change --------------
; Name used for SMB file/data group/data source
smb_data_file: wiperf-smb
;-------------------------------- SMB Section End ----------------------------------
```

## Dashboards

There are no new dashboards in this release. As the number of test targets is now variable, with no upper limit, it is up to individual users to customize the supplied dashboards for their own use.

Going forwards, it is likely I will continue to support the existing 5 instances of each target in any dashboards made available.

## Caveats

Creating a large number of tests may be desirable for certain use-cases, but comes with a few caveats.

Remember that each test is performed sequentially (i.e. no test is started until the previous test completes). The total time taken to finish all tests may become quite long for high numbers of tests, or for tests measuring demanding or poorly performing targets (e.g. large file transfers or targets that time-out).

By default, the poll cycle defined for wiperf is 5 minutes. This can be modified by re-configuring the system cron job used by wiperf to initiate regular polls.

If tests run for longer than the configured poll cycle (e.g. 6 minutes of testing time for a 5 minute poll interval), then a new poll cycle will attempt to start after 5 minutes even though a poll cycle is already in progress. However, the new poll process will detect that a poll cycle is already in progress and exit without performing any tests. This means that you will achieve only half the poll cycles expected, as every 2nd poll cycle will exit without running.

The wiperf poller also has a fail-safe mechanism to try to fix issues in the event of many test failures being detected. It has a watchdog function that will count various system errors and will reboot the probe if they become too high. In the event that many tests are configured that fail in high numbers, then you many observe the probe rebooting periodically due to the watchdog counter being exceeded. This is not an error - this is built in by design to try to fix issues such as being stuck to a remote access point or other network level issues that require a full reboot to clear unknown issues.

## Upgrading
To upgrade from a previous release of wiperf, please consult these instructions in our [upgrade document](probe_upgrade.md).

## Related

Check out this related article: [What's New in version 2.1 ?](whats_new_v2.1.md)



