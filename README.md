[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](https://raw.githubusercontent.com/manbearwiz/youtube-dl-server/master/LICENSE)

# open-weather-map

*open-weather-map* is a Docker image for [*PyOWM*](https://github.com/csparpa/pyowm), a Python wrapper library for [*OpenWeatherMap*](https://openweathermap.org/api).
The docker image is based on [*python:3-alpine*](https://registry.hub.docker.com/_/python/). *OpenWeatherMap* data is queried and logged to a time-series database using [*influxdb-python*](https://github.com/influxdata/influxdb-python).

## Running

### Docker

This example uses the `docker build` command to build the image and the `docker run` command to create a container from that image.

```shell
docker build --tag owm .
docker run -d owm
```

### Docker Compose

This is an example service definition that could be added in `docker-compose.yml`. The *owm* service depends on the *influxdb* service for data logging.

```yml
owm:
    container_name: owm
    build: ./services/owm/
    depends_on:
      - influxdb
    environment:
      - INFLUXDB_HOST=influxdb
      - INFLUXDB_PORT=8086
      - INFLUXDB_DB=iot
      - INFLUXDB_USER=<insert user>
      - INFLUXDB_PASSWORD=<insert password>
      - INFLUXDB_RETENTION_POLICY=raw
      - INFLUXDB_MEASUREMENT=air
      - OWM_API=<insert OpenWeatherMap API key>
      - OWM_LOCATION=<insert location>
      - OWM_INTERVAL=10
    restart: unless-stopped

influxdb:
    container_name: influxdb
    image: influxdb:latest
    environment:
      - INFLUXDB_DB=<insert db>
      - INFLUXDB_DATA_ENGINE=tsm1
      - INFLUXDB_REPORTING_DISABLED=false
      - INFLUXDB_HTTP_AUTH_ENABLED=true
      - INFLUXDB_ADMIN_ENABLED=true
      - INFLUXDB_ADMIN_USER=admin
      - INFLUXDB_ADMIN_PASSWORD=<insert password>
    volumes:
      - ./volumes/influxdb/data:/var/lib/influxdb
      - ./volumes/influxdb/backup:/var/lib/influxdb/backup
    ports:
      - 8086:8086
      - 8083:8083
      - 2003:2003
    restart: always
```
