"""
"""

import os
from pathlib import Path

import yaml


class Config:
    """Flask app configuration class."""

    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")


with open(Path(__file__).absolute().parent.parent / "config.yaml", "r") as config:
    GITHUB_REPOS = yaml.safe_load(config)["github-repos"]
