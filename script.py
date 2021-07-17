# Anything goes here

from irahorecka.models import db, CraigslistHousing
from irahorecka.python.api.craigslisthousing.utils import read_neighborhoods, write_neighborhoods
from irahorecka.python.api.craigslisthousing.clean import clean_craigslist_housing

if __name__ == "__main__":
    # print(read_neighborhoods())
    write_neighborhoods(db.session, CraigslistHousing)
    # clean_craigslist_housing()
