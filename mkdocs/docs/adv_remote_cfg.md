Title: Remote Configuration Server
Authors: Nigel Bowden

# Remote Configuration Server
In wiperf V2, we have added a rudimentary remote configuration server feature to allow the probe's ```config.ini``` file to be changed remotely. The relies on having a private repository in GutHub to store the remote configuration file(s).

To help understand how this can work for you, and to understand the limitations of the solution, here is an overview of the process:

- A private GitHub repo must be created on GitHub - it must be private, otherwise the whole world can read your config files....which is not a good thing (See this doc for details on creating a private repo: [https://docs.github.com/en/github/getting-started-with-github/create-a-repo](https://docs.github.com/en/github/getting-started-with-github/create-a-repo){target=_blank})
- An authorization token for the GitHub repo must be created to allow the probe to access it and read its config file. See this guide to find out how to create a personal access token: [https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token)
- Each time a test cycle starts (i.e. every 5 mins), wiperf will check its local configuration file ```config.ini``` to see if a remote repository is configured
- If a remote repo is configured, then the wiperf process will check to see if it is time to check its remote config file - it doesn't check every poll cycle, to keep the network traffic overhead low.
- If it is time to check the config file, wiperf will pull the config file from the private GutHub repo (using its access token) and overwrite its local config file with its newly retrieved file. This will be used for the next test cycle.

The section of the  ```config.ini``` file that controls remote repo usage is shown below:

```
; central configuration server details
cfg_url: 
cfg_username:
cfg_password:
cfg_token: 
cfg_refresh_interval: 
```

See the following reference guide for an explanation of each field: [config.ini reference guide](config.ini.md#cfg_url)

__Note__: Although the username and password fields are provided to allow GitHun login credentials to be used, this is generally a bad idea.

__Note__: This is an advanced configuration option that requires thorough testing before deploying your probe. Mis-configuration of your remote config file can cause significant operational issues.