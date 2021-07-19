"""
"""

from irahorecka.python.api.craigslist.update.clean import clean_craigslist_housing
from irahorecka.python.api.craigslist.update.score import write_craigslist_housing_score
from irahorecka.python.api.craigslist.read.housing import read_craigslist_housing
from irahorecka.python.api.craigslist.read.neighborhood import read_neighborhoods
from irahorecka.python.api.craigslist.write.housing import write_craigslist_housing
from irahorecka.python.api.craigslist.write.neighborhood import write_neighborhoods

NEIGHBORHOODS = read_neighborhoods()
SFBAY_AREA_KEY = {
    "East Bay": "eby",
    "North Bay": "nby",
    "Peninsula": "pen",
    "San Francisco": "sfc",
    "Santa Cruz": "scz",
    "South Bay": "sby",
}
