
import os
import time

class StatusFile(object):

    '''
    A class to implement status file for FPMS during tests
    '''

    def __init__(self, status_file, file_logger):

        self.status_file =  status_file
        self.file_logger = file_logger

    # write current status msg to file in /tmp for display on FPMS
    def write_status_file(self, text=""):

        if text == '':

            # if no text sent, delete file
            if os.path.exists(self.status_file):
                try:
                    os.remove(self.status_file)
                except Exception as ex:
                    self.file_logger.error("Issue deleting status file: {}.".format(ex))
        else:
            # write status message to file
            try:
                with open(self.status_file, 'w') as statusf:
                    statusf.write(str(text))
            except Exception as ex:
                self.file_logger.error("Issue writing status file: {}.".format(ex))

        time.sleep(1)
        return True