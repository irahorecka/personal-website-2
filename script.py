# Anything goes here

from irahorecka.models import db, CraigslistHousing
from irahorecka.python.api.craigslisthousing.utils import read_neighborhoods, write_neighborhoods

if __name__ == "__main__":
    # print(read_neighborhoods())
    write_neighborhoods(db.session, CraigslistHousing)
