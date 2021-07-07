import json

from irahorecka.python.dynamic_content.github_repos import JSON_PATH, write_github_repos


def read_github_repos():
    """Returns GitHub repos information (scripts/github_/out.json) as a dictionary.
    GitHub repos information is written to `out.json` via `write_github_repos`."""
    with open(JSON_PATH) as file:
        data = json.load(file)
    return data
