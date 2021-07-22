"""
"""

from irahorecka.api.craigslisthousing.read.posts import read_craigslist_housing
from irahorecka.api.craigslisthousing.read.neighborhood import read_neighborhoods
from irahorecka.api.craigslisthousing.write.posts import write_craigslist_housing
from irahorecka.api.craigslisthousing.update.clean import clean_craigslist_housing
from irahorecka.api.craigslisthousing.update.score import write_craigslist_housing_score

NEIGHBORHOODS = read_neighborhoods()
SFBAY_AREA_KEY = {
    "East Bay": "eby",
    "North Bay": "nby",
    "Peninsula": "pen",
    "San Francisco": "sfc",
    "Santa Cruz": "scz",
    "South Bay": "sby",
}
