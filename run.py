"""
/run.py
Ira Horecka - June 2021
~~~~~~~~~~~~~~~~~~~~~~~

A script that starts a Flask web application instance.
"""
import yaml
from pathlib import Path

from irahorecka import app

if __name__ == "__main__":
    # For development purposes only!
    config_path = Path(__file__).absolute().parent / "config.yaml"
    with open(config_path, "r") as config_file:
        config = yaml.safe_load(config_file)

    if config["localhost"]:
        # If you want to host purely locally with ability to use subdomain
        app.config["SERVER_NAME"] = f"localhost:{config['port']}"
        app.run(debug=config["debug"])
    else:
        # Allows access to web page via other devices on the same network
        try:
            app.run(host=config["local-ip"]["mac"], port=config["port"], debug=config["debug"])
        except OSError:
            app.run(host=config["local-ip"]["win"], port=config["port"], debug=config["debug"])
