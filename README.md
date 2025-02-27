<div align="center">
    <img width="35%" alt="data-volume-mqtt" src="./static/logo.svg"/>
</div>

<div align="center">
    <h1>Data Volume MQTT</h1>
    <span>A flask server which gets the remaining data volume from Telekom and sends it to an MQTT broker.</span>
</div>

---

## Use

1. `docker pull ghcr.io/tim0-12432/data-volume-mqtt:latest`
2. `docker run --name data-volume -d -p 8082:8080 --env DATA_VOLUME-MQTT-HOST=192.168.0.2 ghcr.io/tim0-12432/data-volume-mqtt:latest`

## Custom

### Build own image

`sudo docker build . --file Dockerfile --tag tim0-12432/data-volume-mqtt:<tag>`

### Run own container

`sudo docker run --name data-volume -d -p 8082:8080 --env DATA_VOLUME-MQTT-HOST=192.168.0.2 --env DATA_VOLUME-TIME_INTERVAL=60 tim0-12432/data-volume-mqtt:<tag>`

For debugging purposes you can set following environment variables:
`DATA_VOLUME-LOG_LEVEL=DEBUG` and `DATA_VOLUME-APP-DEBUG=True`

## Why

Especially useful when owning a router that uses LTE connection of Telekom related providers.
Some of them are:

- Telekom
- T-Mobile
- Congstar

