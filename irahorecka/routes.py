"""
/enrichment/routes.py
Ira Horecka - June 2021
~~~~~~~~~~~~~~~~~~~~~~~

#
"""

from flask import render_template

from irahorecka import app
from irahorecka.python import get_header, get_body, read_repos


@app.route("/")
def home():
    """Landing page of personal website."""
    content = {
        "title": "Ira Horecka | Home",
        "profile_img": "profile.png",
        "header": get_header("home"),  # Use Jinja syntax s/a `content.header.first`, `content.header.second`, etc.
        "body": get_body("home"),  # Use Jinja syntax s/a `content.body.first`, `content.body.second`, etc.
    }
    return render_template(
        "home.html",
        content=content,
    )


@app.route("/api")
def api():
    """API page of personal website."""
    content = {
        "title": "Ira Horecka | API",
        "profile_img": "me_arrow.png",
        "header": get_header("api"),
        "body": get_body("api"),
    }
    return render_template(
        "layout.html",
        content=content,
    )


@app.route("/projects")
def projects():
    """GitHub projects page of personal website."""
    content = {
        "title": "Ira Horecka | API",
        "profile_img": "me_computing.png",
        "header": get_header("projects"),
        "body": get_body("projects"),
        "repos": read_repos(),
    }
    return render_template(
        "projects.html",
        content=content,
    )
