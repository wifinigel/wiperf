
import datetime
import sys

# module import vars
influx_modules = True
import_err = ''

try:
    import influxdb_client
    from influxdb_client import InfluxDBClient, Point
    from influxdb_client.client.write_api import SYNCHRONOUS
except ImportError as error:
    influx_modules = False
    import_err = error

# TODO: Error checking if write to Influx fails 
# TODO: convert to class

def time_lookup():
    return datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")


def influxexporter(localhost, url, token, bucket, org, dict_data, source, file_logger):

    if not influx_modules:
        file_logger.error(" ********* MAJOR ERROR ********** ")
        file_logger.error("One or more Influx Python modules are not installed on this system. Influx export failed, exiting")
        file_logger.error(import_err)
        sys.exit()

    client = InfluxDBClient(url=url, token=token, org=org, timeout=100)
    write_api = client.write_api(write_options=SYNCHRONOUS)

    now = time_lookup()

    data = []

    # construct data structure to send to InFlux
    for key, value in dict_data.items():

        if key == 'time':
            continue

        data_point = {"measurement": source,
            "tags": { "host": localhost },
            "fields": {key: value},
            "time": now
        }

        data.append(data_point)

    # send to Influx
    file_logger.debug("Data structure sent to Influx:")
    file_logger.debug(data)
    try:
        write_api.write(bucket, org, data)
        file_logger.info("Data sent to InfluxDB. (bucket: {})".format(bucket))
    except Exception as err:
        file_logger.error("Error sending data to InfluxDB: {}".format(err))
    
