"""
/enrichment/routes.py
Ira Horecka - June 2021
~~~~~~~~~~~~~~~~~~~~~~~

#
"""

from flask import render_template

from irahorecka import app


@app.route("/")
def home():
    """Landing page of personal website."""
    return render_template(
        "home.html",
        title="Ira Horecka | Home",
    )
