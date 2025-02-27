from flask import Flask, jsonify, render_template
from flask_minify import Minify
from flask_assets import Environment, Bundle
from config import config_from_env, config_from_dict, ConfigurationSet
from flask.logging import default_handler
from gevent.pywsgi import WSGIServer
import paho.mqtt.client as mqtt
from dotenv import load_dotenv
import requests
import logging


DEFAULT_CONFIG = {
    # information about the server
    "app.host": "0.0.0.0",
    "app.port": 8080,
    "app.debug": False,

    # address of mqtt broker
    "mqtt.host": "localhost",
    "mqtt.port": 1883,

    # log level for debugging
    "log_level": "WARNING",

    # time intervall in seconds
    "time_intervall": 60 * 60 * 12,
}

PREFIX = "DATA_VOLUME"


if __name__ == "__main__":
    load_dotenv()

    cfg = ConfigurationSet(
        config_from_env(prefix=PREFIX, separator="-", lowercase_keys=True),
        config_from_dict(DEFAULT_CONFIG)
    )
    cfg["app.debug"] = str(cfg["app.debug"]).lower() == "true"
    cfg["time_intervall"] = int(cfg["time_intervall"])

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
