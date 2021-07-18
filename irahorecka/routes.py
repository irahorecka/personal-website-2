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
from irahorecka.python import (
    get_header_text,
    get_body_text,
    get_gallery_imgs,
    read_github_repos,
    read_craigslist_housing,
    NEIGHBORHOODS,
    SFBAY_AREA_KEY,
)

with open(Path(__file__).absolute().parent.parent / "config.yaml", "r") as config:
    GITHUB_REPOS = yaml.safe_load(config)["github-repos"]
SCORE_COLORS = {
    "very-poor": "bg-red-400",
    "poor": "bg-red-300",
    "mild-poor": "bg-red-200",
    "neutral": "bg-white",
    "mild-good": "bg-green-200",
    "good": "bg-green-300",
    "very-good": "bg-green-400",
}


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
        "title": "Ira Horecka | Home",
        "profile_img": "profile.png",
        "header": get_header_text("home"),  # Use Jinja syntax s/a `content.header.first`, `content.header.second`, etc.
        "body": get_body_text("home"),  # Use Jinja syntax s/a `content.body.first`, `content.body.second`, etc.
        "images": get_gallery_imgs(),
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


@app.route("/api")
def api():
    """API page of personal website."""
    content = {
        "title": "Ira Horecka | API",
        "profile_img": "me_arrow.png",
        "header": get_header_text("api"),
        "body": get_body_text("api"),
    }
    return render_template("api/api.html", content=content)


@app.route("/api/docs")
def api_docs():
    """Documentation page for personal website's API."""
    content = {
        "title": "Ira Horecka | API Documentation",
        "profile_img": "me_arrow.png",
        "header": get_header_text("api_docs"),
        "body": get_body_text("api_docs"),
    }
    return render_template("api/docs.html", content=content)


@app.route("/api/neighborhoods", methods=["POST"])
def api_neighborhoods():
    area_key = SFBAY_AREA_KEY.get(request.form.get("area", ""))
    neighborhoods = sorted([neighborhood for neighborhood, area in NEIGHBORHOODS.items() if area == area_key])
    return render_template("api/neighborhoods.html", neighborhoods=neighborhoods)


@app.route("/api/submit", methods=["POST"])
def api_table():
    params = {key: value.lower() for key, value in request.form.items() if value and value not in ["-"]}
    params["limit"] = 100
    if params.get("area"):
        params["area"] = SFBAY_AREA_KEY[params["area"].title()]
    try:
        posts = list(read_craigslist_housing(params))
    except ValidationError as e:
        raise InvalidUsage(str(e).capitalize(), status_code=400) from e
    # Replace 'None' with '-' and 1.0 for bedrooms and scores, respectively
    for post in posts:
        if not post["bedrooms"]:
            post["bedrooms"] = "-"
        if not post["score"]:
            post["score"] = 1.0
        post["score_color"] = get_score_color(post["score"])

    return render_template("api/table.html", posts=sorted(posts, key=lambda x: x["score"]))


def get_score_color(score):
    if score == 1.0:
        return SCORE_COLORS["neutral"]
    if score > 2.0:
        return SCORE_COLORS["very-poor"]
    if score > 1.5:
        return SCORE_COLORS["poor"]
    if score > 1.0:
        return SCORE_COLORS["mild-poor"]
    if score < 0.4:
        return SCORE_COLORS["very-good"]
    if score < 0.7:
        return SCORE_COLORS["good"]
    if score < 1.0:
        return SCORE_COLORS["mild-good"]


@app.route("/projects")
def projects():
    """GitHub projects page of personal website."""
    content = {
        "title": "Ira Horecka | API",
        "profile_img": "me_computing.png",
        "header": get_header_text("projects"),
        "body": get_body_text("projects"),
        "repos": read_github_repos(GITHUB_REPOS),
    }
    return render_template("projects.html", content=content)
