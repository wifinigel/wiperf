import speedtest
import sys
import time

class Speedtester(object):
    """
    Class to implement speedtest server tests for wiperf
    """

    def __init__(self, file_logger, platform):

        self.platform = platform
        self.file_logger = file_logger


    def ooklaspeedtest(self, server_id='', DUMMY_DATA=False, DEBUG=False):
        '''
        This function runs the actual speedtest and returns the result
        as a dictionary: 
            { 'ping_time':  ping_time,
            'download_rate': download_rate,
            'upload_rate': upload_rate,
            'server_name': server_name
            }


        Speedtest server list format (dict):
        19079.416816052293: [{'cc': 'NZ',
                        'country': 'New Zealand',
                        'd': 19079.416816052293,
                        'host': 'speed3.snap.net.nz:8080',
                        'id': '6056',
                        'lat': '-45.8667',
                        'lon': '170.5000',
                        'name': 'Dunedin',
                        'sponsor': '2degrees',
                        'url': 'http://speed3.snap.net.nz/speedtest/upload.php',
                        'url2': 'http://speed-dud.snap.net.nz/speedtest/upload.php'},
                        {'cc': 'NZ',
                        'country': 'New Zealand',
                        'd': 19079.416816052293,
                        'host': 'speedtest.wic.co.nz:8080',
                        'id': '5482',
                        'lat': '-45.8667',
                        'lon': '170.5000',
                        'name': 'Dunedin',
                        'sponsor': 'WIC NZ Ltd',
                        'url': 'http://speedtest.wic.co.nz/speedtest/upload.php',
                        'url2': 'http://speedtest.wickednetworks.co.nz/speedtest/upload.php'},
                        {'cc': 'NZ',
                        'country': 'New Zealand',
                        'd': 19079.416816052293,
                        'host': 'speedtest.unifone.net.nz:8080',
                        'id': '12037',
                        'lat': '-45.8667',
                        'lon': '170.5000',
                        'name': 'Dunedin',
                        'sponsor': 'Unifone NZ LTD',
                        'url': 'http://speedtest.unifone.net.nz/speedtest/upload.php'}]
        '''

        if DUMMY_DATA == False:

            # perform Speedtest
            try:
                st = speedtest.Speedtest()
            except Exception as error:
                self.file_logger.error("Speedtest error: {}".format(error))
                return False
            # check if we have specific target server
            if server_id:
                self.file_logger.info("Speedtest info: specific server ID provided for test: {}".format(str(server_id)))
                try:
                    st.get_servers(servers=[server_id])
                except Exception as error:
                    self.file_logger.error("Speedtest error: unable to get details of specified server: {}, reason: {}".format(
                        str(server_id), error))
                    return False
            else:
                try:
                    st.get_best_server()
                except Exception as error:
                    self.file_logger.error("Speedtest error: unable to get best server, reason: {}".format(error))
                    return False

            try:
                download_rate = '%.2f' % (st.download()/1024000)
                self.file_logger.debug("Download rate = " + str(download_rate) + " Mbps")
            except Exception as error:
                self.file_logger.error("Download test error: {}".format(error))
                return False

            try:
                upload_rate = '%.2f' % (st.upload(pre_allocate=False)/1024000)
                self.file_logger.debug("Upload rate = " + str(upload_rate) + " Mbps")
            except Exception as error:
                self.file_logger.error("Upload test error: {}".format(error))
                return False

            results_dict = st.results.dict()
            ping_time = int(results_dict['ping'])
            server_name = results_dict['server']['host']
        else:
            # create dummy data (for speed of testing)
            import random

            ping_time = random.randint(20, 76)
            download_rate = round(random.uniform(30.0, 60.0), 2)
            upload_rate = round(random.uniform(3.0, 8.0), 2)
            server_name = "dummy-speedtest2.warwicknet.com:8080"

        self.file_logger.info('ping_time: {}, download_rate: {}, upload_rate: {}, server_name: {}'.format(
            ping_time, download_rate, upload_rate, server_name))

        return {'ping_time': ping_time, 'download_rate': download_rate, 'upload_rate': upload_rate, 'server_name': server_name}


    def run_tests(self, status_file_obj, check_route_to_dest, config_vars, exporter_obj):

        column_headers = ['time', 'server_name', 'ping_time', 'download_rate_mbps', 'upload_rate_mbps']

        results_dict = {}

        self.file_logger.info("Starting speedtest...")
        status_file_obj.write_status_file("speedtest")

        # check test to Intenet will go via wlan interface
        if check_route_to_dest('8.8.8.8', self.file_logger) == config_vars['wlan_if']:

            self.file_logger.info("Speedtest in progress....please wait.")

            # speedtest returns false if there are any issues
            speedtest_results = self.ooklaspeedtest(config_vars['server_id'])

            if not speedtest_results == False:

                self.file_logger.debug("Main: Speedtest results:")
                self.file_logger.debug(speedtest_results)

                # speedtest results
                results_dict['time'] = int(time.time())
                results_dict['ping_time'] = int(speedtest_results['ping_time'])
                results_dict['download_rate_mbps'] = float(speedtest_results['download_rate'])
                results_dict['upload_rate_mbps'] = float(speedtest_results['upload_rate'])
                results_dict['server_name'] = str(speedtest_results['server_name'])

                self.file_logger.info("Speedtest ended.")

                # dump the results
                data_file = config_vars['speedtest_data_file']
                test_name = "Speedtest"
                exporter_obj.send_results(config_vars, results_dict, column_headers, data_file, test_name, self.file_logger)
            else:
                self.file_logger.error("Error running speedtest - check logs for info.")
        else:
            self.file_logger.error("Unable to run Speedtest as route to Internet not via wireless interface.")
            config_vars['test_issue'] = True
            config_vars['test_issue_descr'] = "Speedtest test failure"
