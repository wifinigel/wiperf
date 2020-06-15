'''
Functions to perform iperf3 tcp & udp tests and return a number of result characteristics

Note this originally used the iperf3 python module, but there were many issuse with the
jitter stats in the udp test, so I decided to use my own wrapper around the iperf 
program itself, which returns results in json format with no issues.
'''
import os
import json
import subprocess
import time

from wiperf.testers.pingtester import PingTester

class IperfTester(object):
    """
    A class to perform a tcp & udp iperf3 tests
    """

    def __init__(self, file_logger, platform):

        self.platform = platform
        self.file_logger = file_logger


    def get_iperf(self):
        '''
        Find the iperf program
        '''
        # This is a little clunky, but the 'which' cmd stopped
        # working in WLANPi image 1.9...after many hours of diagnosing,
        # finally gave up and put this in...
        locations = [
            '/usr/local/bin/iperf3',
            '/usr/bin/iperf3',
            '/bin/iperf3',
            '/sbin/iperf3',
        ]

        for location in locations:

            if os.path.exists(location):
                self.file_logger.debug("Found iperf3 program: {}".format(location))
                return location

        self.file_logger.error("Unable to find iperf3 program")
        return False


    def tcp_iperf_client_test(self, server_hostname, duration=10, port=5201, timeout=2000, debug=False):

        iperf = self.get_iperf()

        if not iperf:
            return False

        protocol = 'tcp'

        iperf_cmd_string = "{} -c {} -t {} -p {} --connect-timeout {} -J".format(iperf, server_hostname, duration, port, timeout)

        self.file_logger.debug("TCP iperf server test params: server: {}, port: {}, protocol: {}, duration: {}, --connect-timeout {}".format(
            server_hostname, port, protocol, duration, timeout))

        # run the test
        try:
            output = subprocess.check_output(
                iperf_cmd_string, stderr=subprocess.STDOUT, shell=True).decode()
        except subprocess.CalledProcessError as exc:
            iperf_json = json.loads(exc.output.decode())
            err_msg = iperf_json['error']
            self.file_logger.error("iperf TCP test error ({}:{}): {}".format(server_hostname, port, err_msg))
            return False

        iperf_json = json.loads(output)

        # extract data
        sent_json = iperf_json['end']['sum_sent']
        recv_json = iperf_json['end']['sum_received']

        # bps
        sent_bps = sent_json['bits_per_second']
        received_bps = recv_json['bits_per_second']

        sent_kbps = sent_bps / 1000
        sent_Mbps = sent_kbps / 1000  # use this

        received_kbps = received_bps / 1000
        received_Mbps = received_kbps / 1000  # use this

        # bytes
        received_bytes = recv_json['bytes']  # use this
        sent_bytes = sent_json['bytes']  # use this

        # retransmits
        retransmits = sent_json.get('retransmits')  # use this

        result = {}
        result['sent_mbps'] = sent_Mbps
        result['received_mbps'] = received_Mbps
        result['sent_bytes'] = sent_bytes
        result['received_bytes'] = received_bytes
        result['retransmits'] = retransmits

        return result

    def calculate_mos(self, rtt_avg_ms, jitter_ms, lost_percent):
        """
        Calculation of approximate MOS score 
        (This was kindly contributed by Mario Gingras, based on this 
        article: https://netbeez.net/blog/impact-of-packet-loss-jitter-and-latency-on-voip/)

        Returns:
            MOS value -- float (1.0 to 4.5)
        """
        #effective_latency=(rtt_avg_ms/2*jitter_ms)+40
        effective_latency=(rtt_avg_ms/2) + (2*jitter_ms) + 10.0

        if effective_latency < 160:
            R = 93.2 - (effective_latency/40)
        else:
            R = 93.2 - ((effective_latency-120)/10)

        R = R - 2.5 * lost_percent

        if R < 0 :
            mos_score=1.0
        elif R <100:
            mos_score = 1 + 0.035*R + 0.000007*R*(R-60)*(100-R)
        else:
            mos_score=4.5
        
        return mos_score

    def udp_iperf_client_test(self, server_hostname, duration=10, port=5201, bandwidth=10000000, timeout=2000, debug=False):

        iperf = self.get_iperf()

        if not iperf:
            return False

        protocol = 'udp'

        self.file_logger.debug("UDP iperf server test params: server: {}, port: {}, protocol: {}, duration: {}, bandwidth: {} --connect-timeout {}".format(
            server_hostname, port, protocol, duration, bandwidth, timeout))

        iperf_cmd_string = "{} -c {} -u -t {} -p {} -b {} --connect-timeout {} -J".format(iperf, server_hostname, duration, port, bandwidth, timeout)

        # run the test
        try:
            output = subprocess.check_output(
                iperf_cmd_string, stderr=subprocess.STDOUT, shell=True).decode()
        except subprocess.CalledProcessError as exc:
            iperf_json = json.loads(exc.output.decode())
            err_msg = iperf_json['error']
            self.file_logger.error("iperf UDP test error ({}:{}): {}".format(
                server_hostname, port, err_msg))
            return False

        iperf_json = json.loads(output)

        # extract data
        bytes = iperf_json['end']['sum']['bytes']
        bps = iperf_json['end']['sum']['bits_per_second']
        jitter_ms = iperf_json['end']['sum']['jitter_ms']
        kbps = bps / 1000
        Mbps = kbps / 1000
        # kB_s = bps / (8 * 1024)
        # MB_s = kB_s / 1024
        packets = iperf_json['end']['sum']['packets']
        lost_packets = iperf_json['end']['sum']['lost_packets']
        lost_percent = iperf_json['end']['sum']['lost_percent']
        # seconds = iperf_json['end']['sum']['seconds']

        result = {}

        result['bytes'] = bytes
        result['mbps'] = Mbps
        result['jitter_ms'] = jitter_ms
        result['packets'] = packets
        result['lost_packets'] = lost_packets
        result['lost_percent'] = lost_percent

        return result

    def run_tcp_test(self, config_vars, status_file_obj, check_route_to_dest, exporter_obj):

            duration = int(config_vars['iperf3_tcp_duration'])
            port = int(config_vars['iperf3_tcp_port'])
            server_hostname = config_vars['iperf3_tcp_server_hostname']

            self.file_logger.info("Starting iperf3 tcp test ({}:{})...".format(server_hostname, str(port)))
            status_file_obj.write_status_file("iperf3 tcp")

            # check test to iperf3 server will go via wlan interface
            if check_route_to_dest(server_hostname, self.file_logger) == config_vars['wlan_if']:

                # run iperf test
                result = self.tcp_iperf_client_test(server_hostname, duration=duration, port=port, debug=False)

                if not result == False:

                    results_dict = {}

                    column_headers = ['time', 'sent_mbps', 'received_mbps', 'sent_bytes', 'received_bytes', 'retransmits']

                    results_dict['time'] = int(time.time())
                    results_dict['sent_mbps'] = round(result['sent_mbps'], 1)
                    results_dict['received_mbps'] = round(result['received_mbps'], 1)
                    results_dict['sent_bytes'] = result['sent_bytes']
                    results_dict['received_bytes'] = result['received_bytes']
                    results_dict['retransmits'] = result['retransmits']

                    # drop abbreviated results in log file
                    self.file_logger.info("Iperf3 tcp results - rx_mbps: {}, tx_mbps: {}, retransmits: {}, sent_bytes: {}, rec_bytes: {}".format(
                        results_dict['received_mbps'], results_dict['sent_mbps'], results_dict['retransmits'], results_dict['sent_bytes'],
                        results_dict['received_bytes']))

                    # dump the results
                    data_file = config_vars['iperf3_tcp_data_file']
                    test_name = "iperf3_tcp"
                    exporter_obj.send_results(config_vars, results_dict, column_headers,
                                data_file, test_name, self.file_logger)

                    self.file_logger.info("Iperf3 tcp test ended.")

                else:
                    self.file_logger.error("Error with iperf3 tcp test, check logs")

            else:
                self.file_logger.error("Unable to run iperf test to {} as route to destination not over wireless interface...bypassing test".format(server_hostname))
                config_vars['test_issue'] = True
                config_vars['test_issue_descr'] = "TCP iperf test failure"
    
    def run_udp_test(self, config_vars, status_file_obj, check_route_to_dest, exporter_obj):

        duration = int(config_vars['iperf3_udp_duration'])
        port = int(config_vars['iperf3_udp_port'])
        server_hostname = config_vars['iperf3_udp_server_hostname']
        bandwidth = int(config_vars['iperf3_udp_bandwidth'])

        self.file_logger.info("Starting iperf3 udp test ({}:{})...".format(server_hostname, str(port)))
        status_file_obj.write_status_file("iperf3 udp")

        if check_route_to_dest(server_hostname, self.file_logger) == config_vars['wlan_if']:

            # Run a ping to the iperf server to get an rtt to feed in to MOS score calc
            ping_obj = PingTester(self.file_logger, platform=self.platform)
            ping_obj.ping_host(server_hostname, 1) # one ping to seed arp cache
            
            ping_result = ping_obj.ping_host(server_hostname, 5)

            # ping results
            if ping_result:
                rtt_avg_ms = round(float(ping_result['rtt_avg']), 2)
            else:
                rtt_avg_ms=0

            # Run the iperf test
            result = self.udp_iperf_client_test(server_hostname, duration=duration, port=port, bandwidth=bandwidth, debug=False)

            if not result == False:

                results_dict = {}

                column_headers = ['time', 'bytes', 'mbps', 'jitter_ms',
                                  'packets', 'lost_packets', 'lost_percent']

                results_dict['time'] = int(time.time())
                results_dict['bytes'] = result['bytes']
                results_dict['mbps'] = round(result['mbps'], 1)
                results_dict['jitter_ms'] = round(result['jitter_ms'], 1)
                results_dict['packets'] = result['packets']
                results_dict['lost_packets'] = result['lost_packets']
                results_dict['lost_percent'] = round(result['lost_percent'], 1)
                results_dict['mos_score']=self.calculate_mos(rtt_avg_ms,round(result['jitter_ms'], 1),round(result['lost_percent'], 1))

                # workaround for crazy jitter figures sometimes seen
                if results_dict['jitter_ms'] > 2000:
                    self.file_logger.error("Received very high jitter value({}), set to none".format(results_dict['jitter_ms']))
                    results_dict['jitter_ms'] = None

                # drop results in log file
                self.file_logger.info("Iperf3 udp results - mbps: {}, packets: {}, lost_packets: {}, lost_percent: {}, jitter: {}, bytes: {}".format(
                    results_dict['mbps'], results_dict['packets'], results_dict['lost_packets'], results_dict['lost_percent'],
                    results_dict['jitter_ms'], results_dict['bytes']))

                # dump the results
                data_file = config_vars['iperf3_udp_data_file']
                test_name = "iperf_udp"
                exporter_obj.send_results(config_vars, results_dict, column_headers, data_file, test_name, self.file_logger)

                self.file_logger.info("Iperf3 udp test ended.")

            else:
                self.file_logger.error("Error with iperf3 udp test, check logs")

        else:
            self.file_logger.error("Unable to run iperf test to {} as route to destination not over wireless interface...bypassing test".format(server_hostname))
            config_vars['test_issue'] = True
            config_vars['test_issue_descr'] = "UDP iperf test failure"