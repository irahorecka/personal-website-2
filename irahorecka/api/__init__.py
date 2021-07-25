"""
"""

from irahorecka.api.craigslisthousing.read.posts import read_craigslist_housing
from irahorecka.api.craigslisthousing.read.neighborhood import read_neighborhoods
from irahorecka.api.craigslisthousing.write.posts import write_craigslist_housing
from irahorecka.api.craigslisthousing.update.clean import clean_craigslist_housing
from irahorecka.api.craigslisthousing.update.score import write_craigslist_housing_score
from irahorecka.api.githubrepos.read import read_github_repos
from irahorecka.api.githubrepos.write import write_github_repos

NEIGHBORHOODS = read_neighborhoods()
# Sourced from python-craigslist-meta
SFBAY_AREA_KEY = {
    "East Bay Area": "eby",
    "North Bay / Marin": "nby",
    "Peninsula": "pen",
    "South Bay Area": "sby",
    "Santa Cruz Co": "scz",
    "City of San Francisco": "sfc",
}
