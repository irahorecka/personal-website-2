"""
/enrichment/__init__.py
Ira Horecka - June 2021
~~~~~~~~~~~~~~~~~~~~~~~

#
"""

import yaml
from pathlib import Path

from flask import Flask
from flask_assets import Bundle, Environment

ROOT_PATH = Path(__file__).absolute().parent.parent
MODULE_PATH = Path(__file__).absolute().parent
with open(ROOT_PATH.joinpath("config.yaml"), "r") as config:
    CONFIG = yaml.safe_load(config)


app = Flask(__name__)

assets = Environment(app)
css = Bundle("src/main.css", output="dist/main.css", filters="postcss")

assets.register("css", css)
css.build()

from irahorecka import routes
