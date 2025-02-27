from config import config_from_env, config_from_dict, ConfigurationSet
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, jsonify, render_template
from flask_assets import Environment, Bundle
from flask.logging import default_handler
from gevent.pywsgi import WSGIServer
from flask_minify import Minify
import paho.mqtt.client as mqtt
from dotenv import load_dotenv
import requests
import datetime
import logging
import time
import json


DEFAULT_CONFIG = {
    # information about the server
    "app.host": "0.0.0.0",
    "app.port": 8080,
    "app.debug": False,

    # address of mqtt broker
    "mqtt.host": "localhost",
    "mqtt.port": 1883,
    "mqtt.devicename": "data_volume_mqtt",

    # log level for debugging
    "log_level": "WARNING",

    # time interval in seconds
    "time_interval": 60 * 60 * 12,
}

PREFIX = "DATA_VOLUME"


if __name__ == "__main__":
    load_dotenv()
    uptime = time.time()

    cfg = ConfigurationSet(
        config_from_env(prefix=PREFIX, separator="-", lowercase_keys=True),
        config_from_dict(DEFAULT_CONFIG)
    )
    cfg["app.debug"] = str(cfg["app.debug"]).lower() == "true"
    cfg["time_interval"] = int(cfg["time_interval"])

    logging.basicConfig(level=cfg.log_level, format='%(name)s: %(levelname)s - %(message)s')
    logging.debug("Configuration: %s", cfg)

    def on_connect(client: mqtt.Client, userdata: any, flags: any, rc: any) -> None:
        logging.info(f"Connected to {cfg.mqtt.host}:{cfg.mqtt.port} with result code {rc}")


    client = mqtt.Client("Data_Volume", clean_session=True)
    client.on_connect = on_connect

    client.connect(cfg["mqtt.host"], cfg["mqtt.port"], 60)

    client.loop_start()

    wz_log = logging.getLogger("werkzeug")
    wz_log.setLevel(cfg.log_level)
    app = Flask("data-volume-mqtt")
    Minify(app, html=True, js=True, cssless=True)
    assets = Environment(app)
    app.logger.addHandler(default_handler)
    app.logger.setLevel(cfg.log_level)

    style_bundle = Bundle("styles.css", filters="cssmin", output="dist/style.min.css", extra={"rel": "stylesheet/css"})
    script_bundle = Bundle("data-fetching.js", filters="jsmin", output="dist/script.min.js", extra={"rel": "script/javascript"})
    assets.register("style_bundle", style_bundle)
    assets.register("script_bundle", script_bundle)
    style_bundle.build()
    script_bundle.build()

    def fetch_data():
        url = "https://pass.telekom.de/api/service/generic/v1/status"
        response = requests.get(url)
        data = response.json()
        return data
    
    def publish_data():
        data = fetch_data()
        time_format = "%Y-%m-%dT%H:%M:%S"
        sensor_data = {
            "Time": datetime.datetime.fromtimestamp(time.time()).strftime(time_format),
            "UsedBytes": data["usedVolume"],
            "TotalBytes": data["initialVolume"],
            "RemainingSeconds": data["remainingSeconds"],
        }
        state_data = {
            "Time": datetime.datetime.fromtimestamp(time.time()).strftime(time_format),
            "Uptime": datetime.datetime.fromtimestamp(time.time() - uptime).strftime("%dT%H:%M:%S"),
            "UptimeSec": time.time() - uptime,
            "POWER": "ON"
        }
        client.publish(f"tele/{cfg['mqtt.devicename']}/SENSOR", json.dumps(sensor_data), qos=1)
        client.publish(f"tele/{cfg['mqtt.devicename']}/STATE", json.dumps(state_data), qos=1)

    scheduler = BackgroundScheduler(daemon=True)
    scheduler.add_job(publish_data, 'interval', seconds=cfg["time_interval"])
    scheduler.start()

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/data", methods=["GET"])
    def get_results():
        data = fetch_data()
        return jsonify(data)

    @app.route("/health", methods=["GET"])
    def health():
        if not client.is_connected():
            logging.error(f"Client is not connected to {cfg.mqtt.host}:{cfg.mqtt.port}!")
            return "1"
        return "0"

    if cfg["app.debug"] == True:
        app.run(host=cfg["app.host"], port=cfg["app.port"], debug=cfg["app.debug"], use_reloader=False)
    else:
        http_server = WSGIServer((cfg["app.host"], cfg["app.port"]), app)
        http_server.serve_forever()
