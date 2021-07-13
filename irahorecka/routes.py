"""
/irahorecka/routes.py
Ira Horecka - July 2021
~~~~~~~~~~~~~~~~~~~~~~~

#
"""

from flask import render_template, request, jsonify

from irahorecka import app
from irahorecka.config import GITHUB_REPOS
from irahorecka.exceptions import InvalidUsage
from irahorecka.python import (
    get_header_text,
    get_body_text,
    get_gallery_imgs,
    read_github_repos,
    read_craigslist_housing,
)


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
    try:
        params = {**{"site": site}, **request.args.to_dict()}
        return jsonify(list(read_craigslist_housing(params)))
    except ValueError as e:
        raise InvalidUsage(str(e).capitalize(), status_code=400) from e


@app.route("/housing/<site>/<area>", subdomain="api")
def api_cl_site_area(site, area):
    """REST-like API for Craigslist housing - querying with Craigslist site
    and area."""
    try:
        params = {**{"site": site, "area": area}, **request.args.to_dict()}
        return jsonify(list(read_craigslist_housing(params)))
    except ValueError as e:
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
    return render_template("api.html", content=content)


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
