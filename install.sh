#!/bin/bash
# Installer for wiperf on WLAN Pi

# Installation script log file
LOG_FILE="/var/log/wiperf_install.log"

# install dir
INSTALL_DIR="/usr/share/wiperf"

SCRIPT_PATH=$(dirname "$(realpath -s "$0")")

echo "(ok) Starting wiperf install process (see $LOG_FILE for details)" | tee $LOG_FILE 

# check we have been dropped in to /usr/share/wiperf before we start
SCRIPT_DIR=`echo  $SCRIPT_PATH || grep '$INSTALL_DIR'` || true
if  [ -z "$SCRIPT_DIR" ]; then
  echo "(fail) Files not installed in $INSTALL_DIR. Exiting." | tee -a $LOG_FILE 
  exit 1
else
  echo "(ok) Files installed in $INSTALL_DIR" | tee -a $LOG_FILE 
fi


# do a local install of the python module using 'pip install python' - exit if errors
echo "(ok) Installing wiperf python module (please wait)..."  | tee -a $LOG_FILE
pip3 install /usr/share/wiperf_poller/ >> $LOG_FILE 2>&1
if [ -z "$?" ]; then
    echo "(fail) pip installation of wiperf_poller failed. Exiting." | tee -a $LOG_FILE 
    exit 1
else
    echo "(ok) wiperf_poller module python installed" | tee -a $LOG_FILE 
fi

# pull & install the Splunk Event collector class
echo "(ok) Cloning the Splunk Event collector class..." | tee -a $LOG_FILE

# take out existing dir (if there)
rm -rf /tmp/Splunk-Class-httpevent

git -C /tmp clone http://github.com/georgestarcher/Splunk-Class-httpevent.git >> $LOG_FILE 2>&1

if [ -z "$?" ]; then
  echo "(fail) Clone of Splunk Python module failed." | tee -a $LOG_FILE
  exit 1
else
  echo "(ok) Python Splunk module cloned OK." | tee -a $LOG_FILE
fi 

# Install the module
echo "(ok) Installing the Splunk Event collector class (please wait)..." | tee -a $LOG_FILE
`pip3 install /tmp/Splunk-Class-httpevent` >> $LOG_FILE 2>&1
if [ -z "$?" ]; then
  echo "(fail) Install of Splunk Python module failed." | tee -a $LOG_FILE
  exit 1
else
  echo "(ok) Splunk Python module installed OK." | tee -a $LOG_FILE
fi


# copy config.ini.default to /etc/wiperf
echo "(ok) Copying config.default.ini to /etc/wiperf..." | tee -a $LOG_FILE
mkdir -p /etc/wiperf  >> $LOG_FILE 2>&1
cp "$SCRIPT_PATH/config.default.ini" /etc/wiperf  >> $LOG_FILE 2>&1
if [ -z "$?" ]; then
  echo "(fail) Copy of config.ini.default failed." | tee -a $LOG_FILE
  exit 1
else
  echo "(ok) Copied OK." | tee -a $LOG_FILE
fi

# move files in ./conf to /etc/wiperf
echo "(ok) Moving conf directory to /etc/wiperf..." | tee -a $LOG_FILE
cp -R "$SCRIPT_PATH/conf" /etc/wiperf  >> $LOG_FILE 2>&1
if [ -z "$?" ]; then
  echo "(fail) Copy of conf directory failed." | tee -a $LOG_FILE
  exit 1
else
  echo "(ok) Copied OK." | tee -a $LOG_FILE
fi

# copy wiperf_switcher to /usr/bin/wiperf_switcher
echo "(ok) Copying wiperf_switcher to /usr/bin/wiperf_switcher..." | tee -a $LOG_FILE
cp "$SCRIPT_PATH/wiperf_switcher" /usr/bin/wiperf_switcher  >> $LOG_FILE 2>&1

if [ -z "$?" ]; then
  echo "(fail) Copy of wiperf_switcher failed." | tee -a $LOG_FILE
  exit 1
else
  echo "(ok) Copied OK." | tee -a $LOG_FILE
  # make sure it can be executed
  chmod 755 /usr/bin/wiperf_switcher
fi

echo "(ok) Install complete." | tee -a $LOG_FILE