"""
/irahorecka/routes.py
Ira Horecka - July 2021
~~~~~~~~~~~~~~~~~~~~~~~

#
"""
from pathlib import Path

import yaml
from flask import render_template, request, jsonify

from irahorecka import app
from irahorecka.exceptions import InvalidUsage, ValidationError
from irahorecka.api import read_craigslist_housing, read_github_repos, NEIGHBORHOODS, SFBAY_AREA_KEY
from irahorecka.utils import tidy_post

with open(Path(__file__).absolute().parent.parent / "config.yaml", "r") as config:
    GITHUB_REPOS = yaml.safe_load(config)["github-repos"]


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    """Handles invalid usage from REST-like api."""
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route("/")
def home():
    """Landing page of personal website."""
    content = {
        "title": "Home",
        "profile_img": "profile.png",
    }
    return render_template("home.html", content=content)


@app.route("/housing/<site>", subdomain="api")
def api_cl_site(site):
    """REST-like API for Craigslist housing - querying with Craigslist site."""
    # Read up to 1,000,000 items if no limit filter is provided.
    params = {**{"site": site}, **request.args.to_dict()}
    try:
        return jsonify(list(read_craigslist_housing(params)))
    except ValidationError as e:
        raise InvalidUsage(str(e).capitalize(), status_code=400) from e


@app.route("/housing/<site>/<area>", subdomain="api")
def api_cl_site_area(site, area):
    """REST-like API for Craigslist housing - querying with Craigslist site
    and area."""
    params = {**{"site": site, "area": area}, **request.args.to_dict()}
    try:
        # Only allow 100 posts to display
        return jsonify(list(read_craigslist_housing(params)))
    except ValidationError as e:
        raise InvalidUsage(str(e).capitalize(), status_code=400) from e


@app.route("/housing")
def api():
    """API page of personal website."""
    content = {
        "title": "Housing",
        "profile_img": "me_arrow.png",
    }
    return render_template("api/housing.html", content=content)


@app.route("/docs", subdomain="api")
def api_docs():
    """Documentation page for personal website's API."""
    content = {
        "title": "Housing API Documentation",
        "profile_img": "me_arrow.png",
    }
    return render_template("api/docs.html", content=content)


@app.route("/api/neighborhoods", methods=["POST"])
def api_neighborhoods():
    """Takes user selection of region and returns neighborhoods within selection."""
    area_key = SFBAY_AREA_KEY.get(request.form.get("area", ""))
    return render_template("api/neighborhoods.html", neighborhoods=NEIGHBORHOODS.get(area_key, tuple()))


@app.route("/api/submit", methods=["POST"])
def api_table():
    params = {key: value.lower() for key, value in request.form.items() if value and value not in ["-"]}
    # 120 posts per query
    params["limit"] = 120
    if params.get("area"):
        params["area"] = SFBAY_AREA_KEY[params["area"].title()]
    try:
        posts = list(read_craigslist_housing(params))
    except ValidationError as e:
        raise InvalidUsage(str(e).capitalize(), status_code=400) from e
    # Replace 'None' with '-' and 1.0 for bedrooms and scores, respectively
    for post in posts:
        # Tidies dictionary through reference
        tidy_post(post)
    return render_template("api/table.html", posts=sorted(posts, key=lambda x: x["score"], reverse=True))


@app.route("/projects")
def projects():
    """GitHub projects page of personal website."""
    content = {
        "title": "Projects",
        "profile_img": "me_computing.png",
        "repos": read_github_repos(GITHUB_REPOS),
    }
    return render_template("projects.html", content=content)
