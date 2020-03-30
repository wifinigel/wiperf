"""
Unit bounce functions

TODO: Convert to object
"""
import os
import sys
import datetime
import subprocess

####################################
# Unit bouncer
####################################
class Bouncer(object):

    def __init__(self, bounce_file, config_vars, file_logger):

        self.bounce_file =  bounce_file
        self.file_logger = file_logger
        self.config_vars = config_vars

    def check_bounce_file(self):

        if os.path.exists(self.bounce_file):
            return True

        return False


    def read_bounce_file(self):

        try:
            with open(self.bounce_file, 'r') as bouncef:
                hour = bouncef.read()
            return hour
        except Exception as ex:
            self.file_logger.error(
                "Issue reading bounce file: {}, exiting...".format(ex))
            sys.exit()


    def write_bounce_file(self, hour):

        try:
            with open(self.bounce_file, 'w') as bouncef:
                bouncef.write(str(hour))
            return True
        except Exception as ex:
            self.file_logger.error(
                "Issue writing bounce file: {}, exiting...".format(ex))
            sys.exit()

    def reboot(self):
        try:
            reboot_output = subprocess.check_output('sudo /sbin/reboot', stderr=subprocess.STDOUT, shell=True).decode()
            self.file_logger.info("Reboot output: {}".format(reboot_output))
            sys.exit()
        except subprocess.CalledProcessError as exc:
            output = exc.output.decode()
            self.file_logger.error("Reboot command had issue: {}.".format(str(output)))
            return False

    def check_for_bounce(self):

        # split out the hours we need to bounce the interface
        bounce_hours = self.config_vars['unit_bouncer'].split(",")
        bounce_hours = [i.strip() for i in bounce_hours]

        # get current time and extract hour
        now = datetime.datetime.now()
        current_hour = '{:02d}'.format(now.hour)

        # check if we have a bounce file that shows time of last bounce
        if self.check_bounce_file():

            last_bounce = self.read_bounce_file()

            # is it time to bounce?
            if current_hour in bounce_hours:

                self.file_logger.info("Time to bounce unit?")

                # possibly time to bounce, have we already bounced?
                if last_bounce != current_hour:

                    self.file_logger.info("Yes, bouncing unit (reboot)")

                    # it's time to reboot
                    self.write_bounce_file(current_hour)
                    self.reboot()
                
                else:
                    self.file_logger.info("No.")

        else:

            # bounce file does not exist, create it with current hour to stop bouncing
            self.file_logger.info("Creating bounce file.")
            self.write_bounce_file(str(current_hour))