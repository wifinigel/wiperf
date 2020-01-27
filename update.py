#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
This script performs a number of functions including:

 - checking for the availability of wiperf updates
 - performing a wiperf update

The checking/update process works as follows:

1. When "update.py check" is run, the contents of the local version.txt file is compared
   to the contents of the latest repo version in the master branch at :
   https://raw.githubusercontent.com/wifinigel/wiperf/master/version.txt

   If the version is repotred in the master branch is greater than the current version
   on the WLAN Pi, then the availability of an upgrade is reported (i.e. the new version number)

   If no upgrade is available, then the test reports a False result

2. When "update.py upgrade is run, the update check is run again (just to be safe), then a 
   git pull of the version tag is performed. This obviously relies on an appropriate version tag
   in the guthub repo being created each time a new release is finalized.

   For example, for new version v0.06:

    git checkout -b v0.06
    git pull origin v0.06

   The pull will update any files that have been updated. This may cause issues conflicts for any 
   files that have been updated locally on the WLAN Pi that now need to be updated from the master
   repo. This should not be an issue for config.ini, as this does not exist in the repo. However, 
   wpa_supplicant.conf is edited by the end-user and could cause an issue if the default
   wpa_supplicant.conf file is ever changed. For this reasn, local changes are always stashed
   before the pull, but the updates to configurable files must be reported in the release notes
   to alert the user that updated files have bene lost.

   Once the pull has been completed, the latest release_notes.txt file must be shown to user to
   alert about new feature and special measures required for manual file updates etc. 

'''

import argparse
import requests
import os
import sys

version_file = '/home/wlanpi/wiperf/version.txt'

if not os.geteuid() == 0:
    print("\n---------------------------------------------")
    print(" You must be root to run this script")
    print(" (use 'sudo update.py') - exiting")
    print("---------------------------------------------\n")
    exit()

###############################################################################
# Main
###############################################################################


def read_version_file():

    global version_file

    if not os.path.exists(version_file):

        print("Unable to find verison file: {} (exiting)".format(version_file))
        sys.exit()

    try:
        with open(version_file, 'r') as versionf:
            version = versionf.read().strip()
        return version
    except Exception as ex:
        print("Issue reading version file: {}, exiting...".format(ex))
        sys.exit()


def main():

    print()
    print("-" * 50)
    print("Update script started...")

    # setup CLI parser
    parser = argparse.ArgumentParser()

    parser.add_argument("--check", action='store_true',
                        help="Check if an update is available")
    parser.add_argument("--update", action='store_true',
                        help="Initiate an update of wiperf software to latest version")

    args = parser.parse_args()

    # if check selected, initiate version check
    if args.check:

        # get the contents of the local version.txt file
        local_version = read_version_file()
        print(local_version)
        # pull the contents of the master repo version.txt

        # end

    print("-" * 50)

###############################################################################
# End main
###############################################################################


if __name__ == "__main__":
    main()
