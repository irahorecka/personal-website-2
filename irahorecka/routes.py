"""
/enrichment/routes.py
Ira Horecka - June 2021
~~~~~~~~~~~~~~~~~~~~~~~

#
"""

from flask import render_template, jsonify

from irahorecka import app
from irahorecka.python import (
    get_header_text,
    get_body_text,
    get_gallery_imgs,
    read_github_repos,
    read_craigslist_housing,
)


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


@app.route("/", subdomain="api")
def rest_api():
    """REST-like API of personal website."""
    return jsonify(list(read_craigslist_housing(limit=1000)))


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
        "repos": read_github_repos(),
    }
    return render_template("projects.html", content=content)
