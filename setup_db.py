import os

from irahorecka.models import db
import irahorecka.api as api

db.create_all()

api.write_github_repos(os.environ.get("GITHUB_TOKEN"))
api.write_craigslist_housing(site="sfbay", areas=["eby", "nby", "sby", "sfc", "pen", "scz"])
api.clean_craigslist_housing()
api.write_craigslist_housing_score(site="sfbay", areas=["eby", "nby", "sby", "sfc", "pen", "scz"])
