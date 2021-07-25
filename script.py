import time

from irahorecka import create_app
from irahorecka.api import clean_craigslist_housing, write_craigslist_housing_score


if __name__ == "__main__":
    t0 = time.time()
    app = create_app()
    with app.app_context():
        clean_craigslist_housing()
        write_craigslist_housing_score("sfbay", ["eby", "nby", "sby", "sfc", "pen", "scz"])
    print(f"Execution time: {'%.2f' % ((time.time() - t0) / 60)} min")
