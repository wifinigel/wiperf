#!/usr/bin/python3
# -*- coding: utf-8 -*-

import datetime

import influxdb_client
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

# TODO: Error checking if write to Influx fails 
# TODO: conditional import of influxdb_client if module available

def time_lookup():
    return datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")


def influxexporter(localhost, url, token, bucket, org, dict_data, source, file_logger):

    client = InfluxDBClient(url=url, token=token, org=org)
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
    write_api.write(bucket, org, data)
    file_logger.info("Data sent to Influx. (bucket: {})".format(bucket))

'''
token = 'BPqy1_9zJ8RsvJFTyYHFMHXMl8ZD1--iIH64xp83SDH-y_0dqzo4pt_zTZ5nFGbtbYuN3ckKKiBGn_LYv6N5Tw=='
url = 'https://eu-central-1-1.aws.cloud2.influxdata.com'
bucket = 'wiperf'
org = '105748af6a5bb862'

host = "orange_wlanpi"
measurement = "speedtest"

client = InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)



data = { 
	"measurement": measurement,
	"tags": { "host": host },
	"fields": {"download": 110},
	"time": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
}

    data = [
        { 
        "measurement": measurement,
        "tags": { "host": host },
        "fields": {"download": 130},
        "time": now
        },
        { 
        "measurement": measurement,
        "tags": { "host": host },
        "fields": {"upload": 20},
        "time": now
        }
    ]
'''

#write_api.write(bucket=bucket, org=org, record=p)