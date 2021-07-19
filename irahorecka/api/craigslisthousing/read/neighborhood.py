"""
"""
from irahorecka.api.craigslisthousing.utils import open_json, NEIGHBORHOOD_PATH


def read_neighborhoods():
    """Returns `neighborhoods.json` as dictionary."""
    return open_json(NEIGHBORHOOD_PATH)
