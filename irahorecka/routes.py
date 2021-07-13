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


@app.route("/housing/sfbay", subdomain="api")
def rest_api():
    """REST-like API of personal website."""
    # As of August 2021, I'm only serving up housing posts from the SF Bay Area
    try:
        return jsonify(list(read_craigslist_housing(request.args)))
    except ValueError as e:
        raise InvalidUsage(str(e).capitalize(), status_code=400)


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
