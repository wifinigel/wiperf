"""
Set of functions to manipulate the process lock file
"""

import sys
import time
import os

class LockFile(object):

    '''
    A class to manipulate the process lock file for the wiperf agent process
    '''

    def __init__(self, lock_file, file_logger):

        self.lock_file = lock_file
        self.file_logger = file_logger

    def lock_file_exists(self):

        if os.path.exists(self.lock_file):
            return True
        
        return False

    def read_lock_file(self):

        try:
            with open(self.lock_file, 'r') as lockf:
                lock_timestamp = lockf.read()
            return lock_timestamp
        except Exception as ex:
            self.file_logger.error("Issue reading lock file: {}, exiting...".format(ex))
            sys.exit()

    def lock_is_old(self):

        lock_timestamp = self.read_lock_file()
        time_now = time.time()
        if (time_now - int(lock_timestamp)) > 540:
            return True
        
        return False
    

    def write_lock_file(self):
        try:
            time_now = int(time.time())
            with open(self.lock_file, 'w') as lockf:
                lockf.write(str(time_now))
            return True
        except Exception as ex:
            self.file_logger.error("Issue writing lock file: {}, exiting...".format(ex))
            sys.exit()

    def break_lock(self):
        
        time_now = int(time.time())
        lock_timestamp = self.read_lock_file()
        self.file_logger.error("Current time: {}, lock file time: {}".format(time_now, lock_timestamp))
        self.write_lock_file()

    def delete_lock_file(self):
        try:
            os.remove(self.lock_file)
            self.file_logger.info("removing lock file")
            return True
        except Exception as ex:
            self.file_logger.error("Issue deleting lock file: {}, exiting...".format(ex))
            sys.exit()

