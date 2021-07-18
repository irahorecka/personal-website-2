# Anything goes here

from os import write
from irahorecka.models import db, CraigslistHousing
from irahorecka.python.api.craigslisthousing.utils import read_neighborhoods, write_neighborhoods
from irahorecka.python.api.craigslisthousing.update import (
    clean_craigslist_housing,
    calculate_post_score,
    write_price_per_area,
)

if __name__ == "__main__":
    # print(read_neighborhoods())
    write_neighborhoods(db.session, CraigslistHousing)
    clean_craigslist_housing()
    write_price_per_area()
