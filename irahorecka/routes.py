"""
/enrichment/routes.py
Ira Horecka - June 2021
~~~~~~~~~~~~~~~~~~~~~~~

#
"""

from flask import render_template

from irahorecka import app
from irahorecka.python import get_header, get_content


@app.route("/")
def home():
    """Landing page of personal website."""
    return render_template(
        "home.html",
        title="Ira Horecka | Home",
        header=get_header("home"),
        content=get_content("home"),
    )


@app.route("/api")
def api():
    """API page of personal website."""
    return render_template(
        "home.html",
        title="Ira Horecka | API",
        header=get_header("api"),
        content=get_content("api"),
    )


@app.route("/projects")
def projects():
    """GitHub projects page of personal website."""
    return render_template(
        "home.html",
        title="Ira Horecka | Projects",
        header=get_header("projects"),
        content=get_content("projects"),
    )


@app.route("/about")
def about():
    """About page of personal website."""
    return render_template(
        "home.html",
        title="Ira Horecka | About",
        header=get_header("about"),
        content=get_content("about"),
    )
