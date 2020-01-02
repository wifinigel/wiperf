'''
Functions to perform iperf3 tcp & udp tests and return a number of result characteristics

Note this originally used the iperf3 python module, but there were many issuse with the
jitter stats in the udp test, so I decided to use my own wrapper around the iperf 
program itself, which returns results in json format with no issues.
'''
import os
import json
import subprocess


def get_iperf(file_logger):
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
            file_logger.info("Found iperf3 program: {}".format(location))
            return location

    file_logger.error("Unable to find iperf3 program")
    return False


def tcp_iperf_client_test(file_logger, server_hostname, duration=10, port=5201, debug=False):

    iperf = get_iperf(file_logger)

    if not iperf:
        return False

    protocol = 'tcp'

    iperf_cmd_string = "{} -c {} -t {} -p {} -J".format(
        iperf, server_hostname, duration, port)

    if debug:
        file_logger.debug("TCP iperf server test params: server: {}, port: {}, protocol: {}, duration: {}".format(
            server_hostname, port, protocol, duration))

    try:
        iperf_output = subprocess.check_output(
            iperf_cmd_string, shell=True).decode()
    except Exception as ex:
        file_logger.error("iperf TCP test error: {}".format(ex))
        return False

    iperf_json = json.loads(iperf_output)

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


def udp_iperf_client_test(file_logger, server_hostname, duration=10, port=5201, bandwidth=10000000, debug=False):

    iperf = get_iperf(file_logger)

    if not iperf:
        return False

    protocol = 'udp'

    if debug:
        file_logger.debug("UDP iperf server test params: server: {}, port: {}, protocol: {}, duration: {}, bandwidth: {}".format(
            server_hostname, port, protocol, duration, bandwidth))

    iperf_cmd_string = "{} -c {} -u -t {} -p {} -b {} -J".format(
        iperf, server_hostname, duration, port, bandwidth)

    # run the test
    try:
        iperf_output = subprocess.check_output(
            iperf_cmd_string, shell=True).decode()
    except Exception as ex:
        file_logger.error("iperf TCP test error: {}".format(ex))
        return False

    iperf_json = json.loads(iperf_output)

    # extract data
    bytes = iperf_json['end']['sum']['bytes']
    bps = iperf_json['end']['sum']['bits_per_second']
    jitter_ms = iperf_json['end']['sum']['jitter_ms']
    kbps = bps / 1000
    Mbps = kbps / 1000
    kB_s = bps / (8 * 1024)
    MB_s = kB_s / 1024
    packets = iperf_json['end']['sum']['packets']
    lost_packets = iperf_json['end']['sum']['lost_packets']
    lost_percent = iperf_json['end']['sum']['lost_percent']
    seconds = iperf_json['end']['sum']['seconds']

    result = {}

    result['bytes'] = bytes
    result['mbps'] = Mbps
    result['jitter_ms'] = jitter_ms
    result['packets'] = packets
    result['lost_packets'] = lost_packets
    result['lost_percent'] = lost_percent

    return result
