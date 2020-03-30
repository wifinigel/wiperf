"""
Watchdog class
"""

import os

class Watchdog(object):

    '''
    A class to implement a watchdog feature for the wiperf agent process
    '''

    def __init__(self, watchdog_file, file_logger):

        self.watchdog_file =  watchdog_file
        self.file_logger = file_logger


    def write_watchdog_count(self, watchdog_count):

        try:
            with open(self.watchdog_file, 'w') as watchf:
                watchf.write(str(watchdog_count))
            return True
        except Exception as ex:
            self.file_logger.error("Issue writing watchdog file: {}.".format(ex))

        return False


    def get_watchdog_count(self):

        if os.path.exists(self.watchdog_file):
            try:
                with open(self.watchdog_file, 'r') as watchf:
                    watchdog_count = watchf.read()
                    return int(watchdog_count)
            except Exception as ex:
                self.file_logger.error("Issue reading watchdog file: {}.".format(ex))

        return False

    # create watchdog file if doesn't exist
    def create_watchdog(self):

        if not os.path.exists(self.watchdog_file):
            try:
                with open(self.watchdog_file, 'w') as watchf:
                    watchf.write(str('0'))
                return True
            except Exception as ex:
                self.file_logger.error("Issue creating watchdog file: {}.".format(ex))

        return False

    # increment watchdog counter due to issue
    def inc_watchdog_count(self):

        watchdog_count = self.get_watchdog_count()
        watchdog_count += 1
        self.write_watchdog_count(watchdog_count)

        return True

    # decrement watchdog counter as test cycle successful
    def dec_watchdog_count(self):

        watchdog_count = self.get_watchdog_count()

        # already zero? Do nothing & return
        if watchdog_count == 0:
            return True

        watchdog_count -= 1
        self.write_watchdog_count(watchdog_count)

        return True