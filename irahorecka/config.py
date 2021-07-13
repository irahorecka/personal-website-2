"""
"""

import os
import yaml
from pathlib import Path

with open(Path(__file__).absolute().parent.parent / "config.yaml", "r") as config:
    GITHUB_REPOS = yaml.safe_load(config)["github-repos"]


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
