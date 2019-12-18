'''
A simple class to perform an iperf3 test and return a number of
result characteristics
'''
from iperf3 import Client

def tcp_iperf_client_test(file_logger, server_hostname, duration=10, port=5201, debug=False):

    # TODO: Handle iperf test failures - return False

    protocol = 'tcp'

    iperf_client = Client()

    iperf_client.server_hostname = server_hostname
    iperf_client.port = port
    iperf_client.protocol = protocol
    iperf_client.duration = duration

    if debug:
        file_logger.debug("TCP iperf server test params: server: {}, port: {}, protocol: {}, duration: {}".format(server_hostname, port, protocol, duration))

    try:
        result = iperf_client.run()
    except Exception as ex:
        file_logger.error("iperf TCP test error: {}".format(ex))

    return result


def udp_iperf_client_test(file_logger, server_hostname, duration=10, port=5201, bandwidth=10000000, debug=False):

    # TODO: Handle iperf test failures - return False

    protocol = 'udp'

    iperf_client = Client()

    iperf_client.server_hostname = server_hostname
    iperf_client.port = port
    iperf_client.protocol = protocol
    iperf_client.duration = duration
    iperf_client.bandwidth = bandwidth

    if debug:
        file_logger.debug("UDP iperf server test params: server: {}, port: {}, protocol: {}, duration: {}, bandwidth: {}".format(server_hostname, port, protocol, duration, bandwidth))

    try:
        result = iperf_client.run()
    except Exception as ex:
        file_logger.error("iperf UDP test error: {}".format(ex))

    return result
