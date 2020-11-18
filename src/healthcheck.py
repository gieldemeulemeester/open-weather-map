#!/usr/bin/env python

import argparse, sys, os, datetime
from influxdb import InfluxDBClient

def get_timestamp():
    client = InfluxDBClient(os.environ['INFLUXDB_HOST'], os.environ['INFLUXDB_PORT'], os.environ['INFLUXDB_USER'], os.environ['INFLUXDB_PASSWORD'], os.environ['INFLUXDB_DB'])
    result = client.query(("SELECT * FROM %s WHERE host='open_weather_map' ORDER by time DESC LIMIT 1") % (os.environ['INFLUXDB_MEASUREMENT']))
    points = result.get_points(measurement=os.environ['INFLUXDB_MEASUREMENT'])
    for point in points: return datetime.datetime.strptime(point['time'], '%Y-%m-%dT%H:%M:%SZ')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check the age of the last measurement.")
    parser.add_argument('-v', '--verbose', action='store_true', dest='isVerbose', help="print debug information")
    parser.add_argument('-i', '--interval', type=int, default=os.environ['OWM_INTERVAL'], help="the expected maximum measurement age")
    args = parser.parse_args()

    if args.interval <= 0: sys.exit(2)

    age = datetime.datetime.utcnow() - get_timestamp()
    print(age)

    if age > datetime.timedelta(minutes=args.interval): sys.exit(1)
