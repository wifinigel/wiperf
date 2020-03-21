import speedtest

def ooklaspeedtest(file_logger, server_id='', DUMMY_DATA=False, DEBUG=False):
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
        import sys

        # perform Speedtest
        try:
            st = speedtest.Speedtest()
        except Exception as error:
            file_logger.error("Speedtest error: {}".format(error))
            return False
        # check if we have specific target server
        if server_id:
            file_logger.info(
                "Speedtest info: specific server ID provided for test: {}".format(str(server_id)))
            try:
                st.get_servers(servers=[server_id])
            except Exception as error:
                file_logger.error("Speedtest error: unable to get details of specified server: {}, reason: {}".format(
                    str(server_id), error))
                return False
        else:
            try:
                st.get_best_server()
            except Exception as error:
                file_logger.error(
                    "Speedtest error: unable to get best server, reason: {}".format(error))
                return False

        try:
            download_rate = '%.2f' % (st.download()/1024000)

            if DEBUG:
                print("Download rate = " + str(download_rate) + " Mbps")
        except Exception as error:
            file_logger.error("Download test error: {}".format(error))
            return False

        try:
            upload_rate = '%.2f' % (st.upload(pre_allocate=False)/1024000)
            if DEBUG:
                print("Upload rate = " + str(upload_rate) + " Mbps")
        except Exception as error:
            file_logger.error("Upload test error: {}".format(error))
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

    file_logger.info('ping_time: {}, download_rate: {}, upload_rate: {}, server_name: {}'.format(
        ping_time, download_rate, upload_rate, server_name))

    return {'ping_time': ping_time, 'download_rate': download_rate, 'upload_rate': upload_rate, 'server_name': server_name}
