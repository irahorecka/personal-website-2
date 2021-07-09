import json

from irahorecka.python.dynamic_content.github_repos import GITHUB_JSON_PATH, write_github_repos


def read_github_repos():
    """Returns GitHub repos information as a dictionary. GitHub repos information is written to
    `GITHUB_JSON_PATH` via `write_github_repos`."""
    with open(GITHUB_JSON_PATH) as file:
        data = json.load(file)
    return data


def read_craigslist_housing():
    """Returns SFBay Craigslist Housing information as a dictionary."""
    pass
