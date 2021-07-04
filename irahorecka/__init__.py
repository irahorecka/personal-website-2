"""
/enrichment/__init__.py
Ira Horecka - June 2021
~~~~~~~~~~~~~~~~~~~~~~~

#
"""

import os
import yaml

from flask import Flask

ROOT_PATH = os.path.dirname(os.path.abspath(os.path.join(__file__, os.pardir)))
MODULE_PATH = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(ROOT_PATH, "config.yaml"), "r") as config:
    CONFIG = yaml.safe_load(config)


app = Flask(__name__)

from irahorecka import routes
