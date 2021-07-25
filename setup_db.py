import os
import time

from irahorecka import create_app
import irahorecka.api as api
from irahorecka.models import db

app = create_app()
with app.app_context():
    t0 = time.time()
    db.create_all()
    api.write_github_repos(os.environ.get("GITHUB_TOKEN"))
    api.write_craigslist_housing(site="sfbay", areas=["eby", "nby", "sby", "sfc", "pen", "scz"])
    api.clean_craigslist_housing()
    api.write_craigslist_housing_score(site="sfbay", areas=["eby", "nby", "sby", "sfc", "pen", "scz"])
    print(f"Execution time: {'%.2f' % ((time.time() - t0) / 60)} min")
