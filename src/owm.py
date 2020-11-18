#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse, sys, os, pyowm, schedule, time
from influxdb import InfluxDBClient
from pyowm.owm import OWM

def log_influx(timestamp, temperature, humidity):
    client = InfluxDBClient(os.environ['INFLUXDB_HOST'], os.environ['INFLUXDB_PORT'], os.environ['INFLUXDB_USER'], os.environ['INFLUXDB_PASSWORD'], os.environ['INFLUXDB_DB'])
    point = [
        {
            "retention_policy": os.environ['INFLUXDB_RETENTION_POLICY'],
            "measurement": os.environ['INFLUXDB_MEASUREMENT'],
            "time": timestamp,
            "tags": {
                "host": "open_weather_map"
            },
            "fields": {
                "temperature": float(temperature),
                "humidity": float(humidity)
            }
        }
    ]
    client.write_points(point)

def get_observed_weather(args):
    owm = OWM(os.environ['OWM_API'])
    mgr = owm.weather_manager()
    observation = mgr.weather_at_place(os.environ['OWM_LOCATION'])
    weather = observation.weather

    if args.isVerbose:
        print(observation)
        print(weather)

    timestamp = weather.reference_time(timeformat='date').strftime("%Y-%m-%d %H:%M:%S")
    temperature = weather.temperature('celsius')['temp']
    humidity = weather.humidity

    print("timestamp: {}, temperature: {}°C, humidity: {}%".format(timestamp, temperature, humidity))

    if args.hasLogging:
        log_influx(timestamp, temperature, humidity)
        if args.isVerbose:
            print("point written to {} database".format(os.environ['INFLUXDB_DB']))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get weather observation from OpenWeatherMap.")
    parser.add_argument('-L', '--log', action='store_true', dest='hasLogging', help="log result to database")
    parser.add_argument('-v', '--verbose', action='store_true', dest='isVerbose', help="print more verbose information")
    parser.add_argument('-i', '--interval', type=int, default=os.environ['OWM_INTERVAL'], help="minutes of delay between repeats, no repeats when zero")
    args = parser.parse_args()

    get_observed_weather(args)

    if args.interval < 0:
        sys.exit(2)
    elif args.interval > 0:
        schedule.every(args.interval).minutes.do(get_observed_weather, args)
        while True:
            schedule.run_pending()
            time.sleep(1)
