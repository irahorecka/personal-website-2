"""
/irahorecka/config.py

Module to store Flask configurations.
"""

import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    """Flask app configuration class."""

    DEBUG = True
    TESTING = False
    SECRET_KEY = os.environ["SECRET_KEY"]
    SQLALCHEMY_DATABASE_URI = os.environ["SQLALCHEMY_DATABASE_URI"]
    SQLALCHEMY_TRACK_MODIFICATIONS = False
