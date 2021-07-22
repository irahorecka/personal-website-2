# Anything goes here

from irahorecka.models import db, CraigslistHousing
from irahorecka.api import clean_craigslist_housing, write_craigslist_housing_score

if __name__ == "__main__":
    # print(read_neighborhoods())
    clean_craigslist_housing()
    write_craigslist_housing_score("sfbay", ["eby", "nby", "sby", "sfc", "pen", "scz"])
