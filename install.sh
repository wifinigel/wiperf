#!/bin/bash
# Installer for wiperf on WLAN Pi

# Installation script log file
LOG_FILE="/var/log/wiperf_install.log"

# install dir
INSTALL_DIR="/usr/share/wiperf"
MODULE_DIR="/usr/share/wiperf_poller"
CFG_DIR="/etc/wiperf"

SCRIPT_PATH=$(dirname "$(realpath -s "$0")")

install () {

  echo "(ok) Starting wiperf install process (see $LOG_FILE for details)" | tee $LOG_FILE 

  # check we can get to pypi
  curl -s --head  -m 2 --connect-timeout 2 --request GET https://pypi.org | head -n 1 | grep '200'
  if [ "$?" != '0' ]; then
    echo "Unable to reach Internet - check connection (exiting)" | tee -a $LOG_FILE 
    exit 1
  fi

  # check git is present
  echo "(ok) Checking we have git available..."
  `git --version`  >> $LOG_FILE 2>&1
  if [ -z "$?" ]; then
    echo "(fail) Unable to proceed as git not installed...please install with command 'apt-get install git' " | tee -a $LOG_FILE
    exit 1
  else
    echo "(ok) Git looks OK"  | tee -a $LOG_FILE
  fi

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
  pip3 install $MODULE_DIR >> $LOG_FILE 2>&1
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

  git -C /tmp clone https://github.com/georgestarcher/Splunk-Class-httpevent.git >> $LOG_FILE 2>&1

  if [ -z "$?" ]; then
    echo "(fail) Clone of Splunk Python module failed." | tee -a $LOG_FILE
    exit 1
  else
    echo "(ok) Python Splunk module cloned OK." | tee -a $LOG_FILE
  fi 

  # Install the module
  echo "(ok) Installing the Splunk Event collector class (please wait)..." | tee -a $LOG_FILE
  pip3 install /tmp/Splunk-Class-httpevent >> $LOG_FILE 2>&1
  if [ -z "$?" ]; then
    echo "(fail) Install of Splunk Python module failed." | tee -a $LOG_FILE
    exit 1
  else
    echo "(ok) Splunk Python module installed OK." | tee -a $LOG_FILE
  fi


  # copy config.ini.default to $CFG_DIR
  echo "(ok) Copying config.default.ini to $CFG_DIR..." | tee -a $LOG_FILE
  mkdir -p $CFG_DIR  >> $LOG_FILE 2>&1
  cp "$SCRIPT_PATH/config.default.ini" $CFG_DIR  >> $LOG_FILE 2>&1
  if [ -z "$?" ]; then
    echo "(fail) Copy of config.ini.default failed." | tee -a $LOG_FILE
    exit 1
  else
    echo "(ok) Copied OK." | tee -a $LOG_FILE
  fi

  # move files in ./conf to $CFG_DIR
  echo "(ok) Moving conf directory to $CFG_DIR..." | tee -a $LOG_FILE
  cp -R "$SCRIPT_PATH/conf" $CFG_DIR  >> $LOG_FILE 2>&1
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
}

uninstall () {
  echo "(ok) Starting wiperf uninstall process (see $LOG_FILE for details)" | tee $LOG_FILE

  # remove python modules
  echo "(ok) Removing Python modules" | tee -a $LOG_FILE
  pip3 uninstall splunk_http_event_collector  >> $LOG_FILE 2>&1
  pip3 uninstall wiperf  >> $LOG_FILE 2>&1

  # remove directories
  echo "(ok) Removing install dir" | tee -a $LOG_FILE
  rm -rf $INSTALL_DIR  >> $LOG_FILE 2>&1
  rm -rf $MODULE_DIR  >> $LOG_FILE 2>&1
  echo "(ok) Removing config dir" | tee -a $LOG_FILE
  rm -rf $CFG_DIR  >> $LOG_FILE 2>&1
  echo "(ok) Removing switcher script" | tee -a $LOG_FILE
  rm -f /usr/bin/wiperf_switcher  >> $LOG_FILE 2>&1

  # remove log files
  echo "(ok) Removing log files" | tee -a $LOG_FILE
  rm -f /var/log/wiperf*.log
  echo "(ok) Done"

}

case "$1" in
  -u)
        uninstall
        ;;
  -i)
        install
        ;;
  *)
        install
        ;;
esac

exit 0