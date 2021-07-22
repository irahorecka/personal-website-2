"""
/enrichment/__init__.py
Ira Horecka - June 2021
~~~~~~~~~~~~~~~~~~~~~~~

#
"""
from flask import Flask
from flask_assets import Bundle, Environment
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from irahorecka.config import Config

db = SQLAlchemy()
css = Bundle("src/main.css", output="dist/main.css", filters="postcss")


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)
    db.init_app(app)

    assets = Environment(app)
    assets.register("css", css)
    css.build()

    from irahorecka.main.routes import main
    from irahorecka.housing.routes import housing

    app.register_blueprint(main)
    app.register_blueprint(housing)

    return app
