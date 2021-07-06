import json

from irahorecka.python.github_.github_ import JSON_PATH, write_repos


def read_repos():
    """Returns GitHub repos information (scripts/github_/out.json) as a dictionary.
    GitHub repos information is written to `out.json` via `write_repos`."""
    with open(JSON_PATH) as file:
        data = json.load(file)
    return data
