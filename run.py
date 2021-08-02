"""
/run.py
~~~~~~~

Starts a Flask web application instance.
"""

from pathlib import Path

import yaml

from irahorecka import create_app

application = create_app()

if __name__ == "__main__":
    # For development purposes only!
    config_path = Path(__file__).absolute().parent / "config.yaml"
    with open(config_path, "r") as config_file:
        config = yaml.safe_load(config_file)

    if config["localhost"]:
        # If you want to host purely locally with ability to use subdomain.
        application.config["SERVER_NAME"] = f"localhost:{config['port']}"
        application.run(debug=config["debug"])
    else:
        # Allows access to web page via other devices on the same network.
        try:
            application.run(host=config["local-ip"]["mac"], port=config["port"], debug=config["debug"])
        except OSError:
            application.run(host=config["local-ip"]["win"], port=config["port"], debug=config["debug"])
