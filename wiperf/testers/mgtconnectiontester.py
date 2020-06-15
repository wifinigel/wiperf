import sys
import time
import subprocess
from socket import gethostbyname

from wiperf.helpers.ethernetadapter import EthernetAdapter

class MgtConnectionTester(object):
    """
    Class to implement network mgt connection tests for wiperf
    """

    def __init__(self, config_vars, file_logger, platform):

        self.config_vars = config_vars
        self.platform = platform
        self.file_logger = file_logger

    def check_connection(self, watchdog_obj, lockf_obj):

        data_transport = self.config_vars['data_transport']
        exporter_type = self.config_vars['exporter_type']
        data_host = self.config_vars['data_host']
        data_port = self.config_vars['data_port']


        # if we are using hec, make sure we can access the hec network port, otherwise we are wasting our time
        if data_transport == 'hec' and exporter_type == 'splunk':
            self.file_logger.info("Checking port connection to Splunk server {}, port: {}".format(data_host, data_port))

            try:
                portcheck_output = subprocess.check_output('/bin/nc -zvw10 {} {}'.format(data_host, data_port), stderr=subprocess.STDOUT, shell=True).decode()
                self.file_logger.info("Port connection to server {}, port: {} checked OK.".format(data_host, data_port))
            except subprocess.CalledProcessError as exc:
                output = exc.output.decode()
                self.file_logger.error("Port check to server failed. Err msg: {} (Exiting...)".format(str(output)))
                watchdog_obj.inc_watchdog_count()
                lockf_obj.delete_lock_file()
                sys.exit()

            return True
        
        elif exporter_type == 'influxdb':
            self.file_logger.info("Checking port connection to InfluxDB server {}, port: {}".format(data_host, data_port))

            try:
                portcheck_output = subprocess.check_output('/bin/nc -zvw10 {} {}'.format(data_host, data_port), stderr=subprocess.STDOUT, shell=True).decode()
                self.file_logger.info("Port connection to server {}, port: {} checked OK.".format(data_host, data_port))
            except subprocess.CalledProcessError as exc:
                output = exc.output.decode()
                self.file_logger.error(
                    "Port check to server failed. Err msg: {} (Exiting...)".format(str(output)))
                watchdog_obj.inc_watchdog_count()
                lockf_obj.delete_lock_file()
                sys.exit()

            return True

        elif exporter_type == 'influxdb2':
            self.file_logger.info("Checking port connection to InfluxDB2 server {}, port: {}".format(data_host, data_port))

            try:
                portcheck_output = subprocess.check_output('/bin/nc -zvw10 {} {}'.format(data_host, data_port), stderr=subprocess.STDOUT, shell=True).decode()
                self.file_logger.info("Port connection to server {}, port: {} checked OK.".format(data_host, data_port))
            except subprocess.CalledProcessError as exc:
                output = exc.output.decode()
                self.file_logger.error(
                    "Port check to server failed. Err msg: {} (Exiting...)".format(str(output)))
                watchdog_obj.inc_watchdog_count()
                lockf_obj.delete_lock_file()
                sys.exit()

            return True
        
        else:
            self.file_logger.info("Unknown exporter type configured in config.ini: {} (exiting)".format(exporter_type))
            sys.exit()


