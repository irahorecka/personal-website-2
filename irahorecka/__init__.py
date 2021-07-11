"""
/enrichment/__init__.py
Ira Horecka - June 2021
~~~~~~~~~~~~~~~~~~~~~~~

#
"""
from flask import Flask
from flask_assets import Bundle, Environment
from flask_sqlalchemy import SQLAlchemy

from irahorecka.config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

assets = Environment(app)
css = Bundle("src/main.css", output="dist/main.css", filters="postcss")
assets.register("css", css)
css.build()

from irahorecka import routes
