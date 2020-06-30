#!/bin/bash
# Installer for wiperf on WLAN Pi & RPi

# Installation script log file
LOG_FILE="/var/log/wiperf_install.log"

# define global vars
CLONE_DIR="/usr/share"
INSTALL_DIR="$CLONE_DIR/wiperf"
CFG_DIR="/etc/wiperf"
GITHUB_REPO="https://github.com/wifinigel/wiperf.git"
GITHUB_BRANCH='dev'
OPERATION=$1
PLATFORM=$2

# install function
install () {

  echo "(ok) Starting wiperf install process for $PLATFORM (see $LOG_FILE for details)" | tee -a $LOG_FILE 

  # Check which platform we're installing for
  if ! [[ $PLATFORM =~ ^(wlanpi|rpi)$ ]]; then
    echo "Unknown (or no) platform supplied (exiting)"
    exit 1
  fi

  ### check we can get to pypi before staring
  curl -s --head  -m 2 --connect-timeout 2 --request GET https://pypi.org | head -n 1 | grep '200'  >> $LOG_FILE 2>&1
  if [ "$?" != '0' ]; then
    echo "Unable to reach Internet - check connection (exiting)" | tee -a $LOG_FILE 
    exit 1
  fi

  ### check git is present
  echo "(ok) Checking we have git available..."
  git --version  >> $LOG_FILE 2>&1
  if [ "$?" != '0' ]; then
    echo "(fail) Unable to proceed as git not installed...please install with command 'apt-get install git' " | tee -a $LOG_FILE
    exit 1
  else
    echo "(ok) Git looks OK"  | tee -a $LOG_FILE
  fi

  ### check iperf3 is present
  echo "(ok) Checking we have iperf3 available..."
  iperf3 -v  >> $LOG_FILE 2>&1
  if [ "$?" != '0' ]; then
    echo "(fail) Unable to proceed as iperf3 not installed...please install with command 'apt-get install iperf3' " | tee -a $LOG_FILE
    exit 1
  else
    echo "(ok) iperf3 looks OK"  | tee -a $LOG_FILE
  fi

  # check that pip3 is available
  echo "(ok) Checking we have pip3 available..."
  pip3 -v  >> $LOG_FILE 2>&1
  if [ "$?" != '0' ]; then
    echo "(fail) Unable to proceed as pip3 not installed...please install with command 'apt-get install python3-pip' " | tee -a $LOG_FILE
    exit 1
  else
    echo "(ok) pip3 looks OK"  | tee -a $LOG_FILE
  fi

  ### install the wiperf poller from PyPi - exit if errors
  echo "(ok) Installing wiperf python module (please wait)..."  | tee -a $LOG_FILE
  pip3 install wiperf_poller >> $LOG_FILE 2>&1
  if [ "$?" != '0' ]; then
      echo "(fail) pip installation of wiperf_poller failed. Exiting." | tee -a $LOG_FILE 
      exit 1
  else
      echo "(ok) wiperf_poller module python installed" | tee -a $LOG_FILE 
  fi

  ### pull & install the Splunk Event collector class
  echo "(ok) Cloning the Splunk Event collector class..." | tee -a $LOG_FILE
  # take out existing dir (if there)
  rm -rf /tmp/Splunk-Class-httpevent
  repo_src="https://github.com/wifinigel/Splunk-Class-httpevent.git"
  #repo_src="https://github.com/georgestarcher/Splunk-Class-httpevent.git"
  git -C /tmp clone $repo_src >> $LOG_FILE 2>&1

  if [ "$?" != '0' ]; then
    echo "(fail) Clone of Splunk Python module failed." | tee -a $LOG_FILE
    exit 1
  else
    echo "(ok) Python Splunk module cloned OK." | tee -a $LOG_FILE
  fi 

  ### Install the Splunk collector module
  echo "(ok) Installing the Splunk Event collector class (please wait)..." | tee -a $LOG_FILE
  pip3 install /tmp/Splunk-Class-httpevent >> $LOG_FILE 2>&1
  if [ -z "$?" ]; then
    echo "(fail) Install of Splunk Python module failed." | tee -a $LOG_FILE
    exit 1
  else
    echo "(ok) Splunk Python module installed OK." | tee -a $LOG_FILE
  fi

  ### Pull in the wiperf github code
  echo "(ok) Cloning GitHub wiperf repo (please wait)..." | tee -a $LOG_FILE
  # get rid of the local copy if already exists (in case installing over the top)
  rm -rf $INSTALL_DIR >> $LOG_FILE 2>&1
  git -C $CLONE_DIR clone $GITHUB_REPO -b $GITHUB_BRANCH >> $LOG_FILE 2>&1
  if [ "$?" != '0' ]; then
    echo "(fail) Clone of GitHub repo failed." | tee -a $LOG_FILE
    exit 1
  else
    echo "(ok) Cloned OK." | tee -a $LOG_FILE
  fi

  ### copy config.ini.default to $CFG_DIR
  echo "(ok) Moving config.default.ini to $CFG_DIR..." | tee -a $LOG_FILE
  mkdir -p $CFG_DIR  >> $LOG_FILE 2>&1
  mv "$INSTALL_DIR/config.default.ini" $CFG_DIR  >> $LOG_FILE 2>&1
  if [ "$?" != '0' ]; then
    echo "(fail) Copy of config.ini.default failed." | tee -a $LOG_FILE
    exit 1
  else
    echo "(ok) Copied OK." | tee -a $LOG_FILE
  fi

  ### move files in ./conf to $CFG_DIR for wlanpi, remove 'conf' dir for rpi
  echo "(ok) Moving conf directory to $CFG_DIR..." | tee -a $LOG_FILE
  mv "$INSTALL_DIR/conf" $CFG_DIR  >> $LOG_FILE 2>&1
  
  if [ -z "$?" ]; then
    echo "(fail) Copy of conf directory failed." | tee -a $LOG_FILE
    exit 1
  else
    echo "(ok) Copied OK." | tee -a $LOG_FILE
  fi
  
  if [ "$PLATFORM" = 'rpi' ]; then
    # remove the conf dir if rpi, as don't need it
    echo "(ok) Removing conf directory $CFG_DIR/conf...(not needed on RPi)" | tee -a $LOG_FILE
    rm -rf $CFG_DIR/conf >> $LOG_FILE 2>&1
  fi 

  # if we have old config files, copy them back im
  if [ -e ".${CFG_DIR}/config.ini"] ; then
    echo "(ok) Restoring old config files..." | tee -a $LOG_FILE
    # copy files back in to retain old config & connectivity
    cp -R ".${CFG_DIR}/*" ${CFG_DIR}  >> $LOG_FILE 2>&1
  fi

  ### copy across the wiperf switcher if this is a WLAN Pi, remove if rpi 
  if [ "$PLATFORM" = 'wlanpi' ]; then
    # copy wiperf_switcher to /usr/bin/wiperf_switcher
    echo "(ok) Moving wiperf_switcher to /usr/bin/wiperf_switcher..." | tee -a $LOG_FILE
    mv "$INSTALL_DIR/wiperf_switcher" /usr/bin/wiperf_switcher  >> $LOG_FILE 2>&1

    if [ "$?" != '0' ]; then
      echo "(fail) Copy of wiperf_switcher failed." | tee -a $LOG_FILE
      exit 1
    else
      echo "(ok) Copied OK." | tee -a $LOG_FILE
      # make sure it can be executed
      chmod 755 /usr/bin/wiperf_switcher
    fi
  else
      # remove the conf dir if rpi, as don't need it
      echo "(ok) Removing wiperf_switcher file...(not needed on RPi)" | tee -a $LOG_FILE
      rm -f $INSTALL_DIR/wiperf_switcher >> $LOG_FILE 2>&1
  fi

  #TODO: Add series of tests to check out the final env
  
  echo "(ok) Install complete." | tee -a $LOG_FILE

  if [ "$PLATFORM" = 'wlanpi' ]; then
    echo ""
    echo "================================================="
    echo "Don't forget to modify the following files before"
    echo "switching in to wiperf mode:"
    echo ""
    echo " 1. Copy default cfg file to live cfg:  sudo cp $CFG_DIR/config.default.ini $CFG_DIR/config.ini"
    echo " 2. Edit the cfg file for your env: sudo nano $CFG_DIR/config.ini"
    echo " 3. Edit the WLAN config file for your env: sudo nano $CFG_DIR/conf/etc/wpa_supplicant/wpa_supplicant.conf" 
    echo "    (add WLAN info)"
    echo " 4. Reboot the WLAN Pi before first-use from fpms: sudo sync; sudo reboot"
    echo "================================================="
    echo ""
  else
    echo ""
    echo "================================================="
    echo "Don't forget to modify the following files before"
    echo "trying to use wiperf:"
    echo ""
    echo " 1. Edit wireless auth settings: sudo nano /etc/wpa_supplicant/wpa_supplicant.conf"
    echo " 2. Edit wlan0 settings: sudo nano /etc/network/interfaces" 
    echo " 3. Copy default cfg file to live cfg:  sudo cp $CFG_DIR/config.default.ini $CFG_DIR/config.ini"
    echo " 4. Edit the cfg file for your env: nano $CFG_DIR/config.ini"
    echo " 5. Add a cron job to run wiperf regularly, e.g. crontab -e (add line below)"
    echo "    0-59/5 * * * * /usr/bin/python3 /usr/share/wiperf/wiperf_run.py > /var/log/wiperf_cron.log 2>&1"
    echo " 6. If you are running several probes on a network, change their hostnames to be unique:"
    echo "    sudo nano /etc/hostname (change raspberrypi to your req hostname)"
    echo "    sudo nano /etc/hosts (change raspberrypi to your req hostname)"
    echo "    sudo reboot"
    echo "================================================="
    echo ""
  fi
}

uninstall () {
  echo "(ok) Starting wiperf uninstall process (see $LOG_FILE for details)" | tee -a $LOG_FILE
  cd /tmp

  # remove python modules
  echo "(ok) Removing Python modules" | tee -a $LOG_FILE
  echo "(ok) ...splunk_http_event_collector" | tee -a $LOG_FILE
  pip3 uninstall -y Splunk-HEC  >> $LOG_FILE 2>&1
  echo "(ok) ...wiperf_poller" | tee -a $LOG_FILE
  pip3 uninstall -y wiperf_poller  >> $LOG_FILE 2>&1

  # remove directories
  echo "(ok) Removing install dir" | tee -a $LOG_FILE
  rm -rf $INSTALL_DIR  >> $LOG_FILE 2>&1
  echo "(ok) Removing config dir" | tee -a $LOG_FILE
  mv $CFG_DIR ".${CFG_DIR}" >> $LOG_FILE 2>&1
  #rm -rf $CFG_DIR  >> $LOG_FILE 2>&1
  echo "(ok) Removing switcher script" | tee -a $LOG_FILE
  rm -f /usr/bin/wiperf_switcher  >> $LOG_FILE 2>&1

  # remove log files
  echo "(ok) Removing log files" | tee -a $LOG_FILE
  rm -f /var/log/wiperf*.log
  echo "(ok) Done"
}

upgrade () {

# Check which platform we're installing for
  if ! [[ $PLATFORM =~ ^(wlanpi|rpi)$ ]]; then
    echo "Unknown (or no) platform supplied (exiting)"
    exit 1
  fi
  
  echo "(ok) wiperf will now be unistalled, then re-installed with a new version"

  ### check we can get to pypi before staring
  echo "(ok) checking we can get to the Internet before we start..."  | tee $LOG_FILE
  curl -s --head  -m 2 --connect-timeout 2 --request GET https://pypi.org | head -n 1 | grep '200'  >> $LOG_FILE 2>&1
  if [ "$?" != '0' ]; then
    echo "(fail) Unable to reach Internet - check connection (exiting)" | tee -a $LOG_FILE 
    exit 1
  fi

  # kick off the uninstall
  uninstall

  # install new code
  echo "(ok) Installing latest version of wiperf..."
  install 

  exit 0
}

case "$1" in
  install)
        install
        ;;
  upgrade)
        upgrade
        ;;
  remove)
        uninstall
        ;;
  *)
        echo "Usage: install.sh {-i | -u | -r} {wlanpi | rpi}"
        echo ""
        echo "  setup.sh install : run installer"
        echo "  setup.sh upgrade : upgrade"
        echo "  setup.sh remove  : remove wiperf completely"
        echo ""
        exit 0
        ;;
esac

exit 0