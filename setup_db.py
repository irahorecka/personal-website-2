import os

from irahorecka.models import db, CraigslistHousing
import irahorecka.python.content as ct
import irahorecka.python.api as api

db.create_all()

ct.write_github_repos(os.environ.get("GITHUB_TOKEN"))
api.write_craigslist_housing(site="sfbay", areas=["eby", "nby", "sby", "sfc", "pen", "scz"])
api.clean_craigslist_housing()
api.write_neighborhoods(db.session, CraigslistHousing)
