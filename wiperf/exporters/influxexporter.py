import datetime
import sys

# module import vars
influx_modules = True
import_err = ''

try:
    from influxdb import InfluxDBClient
except ImportError as error:
    influx_modules = False
    import_err = error

# TODO: Error checking if write to Influx fails 
# TODO: convert to class

def time_lookup():
    return datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")


def influxexporter(localhost, host, port, username, password, database, dict_data, source, file_logger):

    if not influx_modules:
        file_logger.error(" ********* MAJOR ERROR ********** ")
        file_logger.error("One or more Influx Python .are not installed on this system. Influx export failed, exiting")
        file_logger.error("(Execute the following command from the command line of the WLAN Pi: 'sudo pip3 install influxdb')")
        file_logger.error(import_err)
        sys.exit()

    #client = InfluxDBClient(host, port, database, username, password, timeout=100, ssl=True, verify_ssl=True)
    client = InfluxDBClient(host, port, username, password, database, timeout=100)
    file_logger.debug("Creating InfluxDB API client...")
    file_logger.debug("Remote host: -{}-".format(host))
    file_logger.debug("Port: -{}-".format(port))
    file_logger.debug("Database: -{}-".format(database))
    file_logger.debug("User: -{}-".format(username))

    data_point = {
        "measurement": source,
        "tags": { "host": localhost },
        "fields": {},
    }

    fields_dict = {}

    # construct data structure to send to InFlux
    for key, value in dict_data.items():

        if key == 'time':
            continue

        fields_dict[key] = value

    data_point['fields'] = fields_dict

    # send to Influx
    try:
        if client.write_points([data_point]):    
            file_logger.info("Data sent to influx OK")
        else:
            file_logger.info("Issue with sending data sent to influx...")

    except Exception as err:
        file_logger.error("Issue sending data to Influx: {}".format(err))
    
    file_logger.debug("Data structure sent to Influx:")
    file_logger.debug(data_point)

    
