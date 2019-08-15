'''
A simple class to perform an network ICMP Ping and return a number of
result characteristics
'''
from __future__ import print_function

class Pinger(object):
    '''
    A class to ping a host - a basic wrapper around a CLI ping command
    '''

    def __init__(self, platform="rpi", debug=False):

        self.platform = platform
        self.debug = debug

        self.host = ''
        self.pkts_tx = ''
        self.pkts_rx = ''
        self.pkt_loss = ''
        self.test_time = ''
        self.rtt_min = ''
        self.rtt_avg = ''
        self.rtt_max = ''
        self.rtt_mdev = ''


    def ping_host(self, host, count):
        '''
        This function will run a ping test and return an analysis of the results

        If the ping fails, a False condition is returned with no further
        information. If the ping succeeds, the following dictionary is returned:

        {   'host': self.host,
            'pkts_tx': self.pkts_tx,
            'pkts_rx': self.pkts_rx,
            'pkt_loss': self.pkt_loss,
            'test_time': self.test_time,
            'rtt_min': self.rtt_min,
            'rtt_avg': self.rtt_max,
            'rtt_max': self.rtt_max,
            'rtt_mdev': self.rtt_mdev}

        '''
        import re
        import subprocess
        from sys import stderr

        self.host = host

        if self.debug:
            print("Pinging host: " + str(host) + " (count=" + str(count) +")")

        # Execute the ping
        try:
            ping_output = (subprocess.check_output(["/bin/ping", "-q", "-c " \
            + str(count), host])).splitlines()
        except Exception as error:
            if self.debug:
                print("Hit an error with ping: ")
                print(error)

            stderr.write("Error with running ping command: " + str(error))

            # Things have gone bad - we just return a false status
            return False


        if self.debug:
            print("Ping command output:")
            print(ping_output)

        packets_summary_str = ping_output[3]

        # Extract packets transmitted
        pkts_tx_re = re.search('(\d+) packets transmitted', packets_summary_str)
        if pkts_tx_re is None:
            self.pkts_tx = "NA"
        else:
            self.pkts_tx = pkts_tx_re.group(1)

        # Extract packets received
        pkts_rx_re = re.search('(\d+) received', packets_summary_str)
        if pkts_rx_re is None:
            self.pkts_rx = "NA"
        else:
            self.pkts_rx = pkts_rx_re.group(1)

        # Extract packet loss
        pkt_loss_re = re.search('(\d+)\% packet loss', packets_summary_str)
        if pkt_loss_re is None:
            self.pkt_loss = "NA"
        else:
            self.pkt_loss = pkt_loss_re.group(1)

        # Extract test time (duration)
        test_time_re = re.search('time (\d+)ms', packets_summary_str)
        if test_time_re is None:
            self.test_time = "NA"
        else:
            self.test_time = test_time_re.group(1)

        if self.debug:
            print("Packets transmitted: " + str(self.pkts_tx))
            print("Packets received: " + str(self.pkts_rx))
            print("Packet loss(%): " + str(self.pkt_loss))
            print("Test duration (mS): " + str(self.test_time))

        perf_summary_str = ping_output[4]
        perf_data_re = re.search('= ([\d\.]+?)\/([\d\.]+?)\/([\d\.]+?)\/([\d\.]+)', \
        perf_summary_str)

        if test_time_re is None:
            self.rtt_min = "NA"
            self.rtt_avg = "NA"
            self.rtt_max = "NA"
            self.rtt_mdev = "NA"
        else:
            self.rtt_min = perf_data_re.group(1)
            self.rtt_avg = perf_data_re.group(2)
            self.rtt_max = perf_data_re.group(3)
            self.rtt_mdev = perf_data_re.group(4)

        if self.debug:
            print("rtt_min : " + str(self.rtt_min))
            print("rtt_avg : " + str(self.rtt_avg))
            print("rtt_max : " + str(self.rtt_max))
            print("rtt_mdev : " + str(self.rtt_mdev))

        return {
            'host': self.host,
            'pkts_tx': self.pkts_tx,
            'pkts_rx': self.pkts_rx,
            'pkt_loss': self.pkt_loss,
            'test_time': self.test_time,
            'rtt_min': self.rtt_min,
            'rtt_max': self.rtt_max,
            'rtt_avg': self.rtt_avg,
            'rtt_mdev': self.rtt_mdev}

    def get_host(self):
        ''' Get host name/address '''
        return self.host

    def get_pkts_tx(self):
        ''' Get transmitted packet count'''
        return self.pkts_tx

    def get_pkts_rx(self):
        ''' Get received packet count '''
        return self.pkts_rx

    def get_pkt_loss(self):
        ''' Get percentage packet loss detected during test '''
        return self.pkt_loss

    def get_test_time(self):
        ''' Get the test duration in seconds '''
        return self.test_time

    def get_rtt_min(self):
        ''' Get the minimum round trip time observed during the test '''
        return self.rtt_min

    def get_rtt_max(self):
        ''' Get the maximum round trip time observed during the test '''
        return self.rtt_max

    def get_rtt_avg(self):
        ''' Get the average round trip time observed during the test '''
        return self.rtt_avg

    def get_rtt_mdev(self):
        ''' Get the median round trip time observed during the test '''
        return self.rtt_mdev
