# -*- coding: utf-8 -*-

import os
from shutil import copyfile
import sys
from PyInquirer import prompt as ask_questions

from wiperf.config.general import general_section
from wiperf.helpers.config import read_local_config
from wiperf.helpers.filelogger import FileLogger

answers = {}

def main():

    # define useful system files
    this_dir = os.path.dirname(os.path.realpath(__file__))

    config_file = this_dir + "/config.ini"
    default_config_file = this_dir + "/config.default.ini"
    log_file = this_dir + "/logs/config.log"

    # set up our log file & initialize
    file_logger = FileLogger(log_file)
    file_logger.info("*****************************************************")
    file_logger.info(" Starting logging...")
    file_logger.info("*****************************************************")

    # if config.ini doesn't exist, clone it from default config file
    if not os.path.exists(config_file):
        try:
            file_logger.info("Config file does not exist, creating...")
            copyfile(default_config_file, config_file)
        except IOError as e:
            file_logger.error("Unable to copy file. {}".format(e))
            exit(1)
        except:
            file_logger.error("Unexpected error: {}".format(sys.exc_info()))
            exit(1)

    # read the config file
    (config_vars, config_obj) = read_local_config(config_file, file_logger)

    # Show the sections menu and choose which section to update
    #
    # 1. Global
    # 2. Management platform
    # 3. Test interval
    #

    while True:

        print("\n========================================")
        print("          **** MAIN MENU **** ")
        print("========================================\n")
    
        questions = [
            {
                'type': 'rawlist',
                'name': 'main_menu',
                'message': 'Choose section to configure: ',
                'choices': ["Global Options", "Management pltaform", "Test Interval", ]
            }
        ]

        answers = ask_questions(questions)

        print("\n\n")
    
        if answers['main_menu'] == "Global Options":
            gen_sect_answers = general_section(config_vars, config_obj, config_file)
            #print("Entered data: ")
            #print( gen_sect_answers)

if __name__ == "__main__":
    main()

