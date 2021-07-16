"""
"""

from irahorecka.python.api.craigslisthousing.read import read_craigslist_housing
from irahorecka.python.api.craigslisthousing.write import write_craigslist_housing
from irahorecka.python.api.craigslisthousing.utils import read_neighborhoods, write_neighborhoods

NEIGHBORHOODS = read_neighborhoods()
SFBAY_AREA_KEY = {
    "East Bay": "eby",
    "North Bay": "nby",
    "Peninsula": "pen",
    "San Francisco": "sfc",
    "Santa Cruz": "scz",
    "South Bay": "sby",
}
