import json

from .github_ import JSON_PATH, write_user_repos


def read_user_repos():
    """Returns user repos information (scripts/github_/out.json) as a dictionary."""
    with open(JSON_PATH) as file:
        data = json.load(file)
    return data
