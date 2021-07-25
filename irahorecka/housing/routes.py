"""
/irahorecka/routes.py
Ira Horecka - July 2021
~~~~~~~~~~~~~~~~~~~~~~~

#
"""
from datetime import datetime

from flask import render_template, request, jsonify, Blueprint

from irahorecka.api import read_craigslist_housing, NEIGHBORHOODS, SFBAY_AREA_KEY
from irahorecka.exceptions import InvalidUsage, ValidationError
from irahorecka.housing.utils import tidy_posts, read_docs

housing = Blueprint("housing", __name__)


@housing.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    """Handles invalid usage from REST-like api."""
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@housing.route("/housing")
def home():
    """API page of personal website."""
    content = {
        "title": "Housing",
        "profile_img": "me_arrow.png",
    }
    return render_template("housing/index.html", content=content)


@housing.route("/housing/neighborhoods", methods=["POST"])
def neighborhoods():
    """Takes user selection of region and returns neighborhoods within selection.
    Notice the routing, it is outside of /housing. This is because neighborhoods are agnostic
    to classified listings' categories."""
    area_key = SFBAY_AREA_KEY.get(request.form.get("area", "").lower())
    return render_template("housing/neighborhoods.html", neighborhoods=NEIGHBORHOODS.get(area_key, tuple()))


@housing.route("/housing/query", methods=["POST"])
def query():
    parsed_params = parse_query_form(request.form)
    posts = list(read_craigslist_housing(parsed_params))
    return render_template(
        "housing/table.html", posts=sorted(tidy_posts(posts), key=lambda x: x["score"], reverse=True)
    )


@housing.route("/housing/query_new", methods=["POST"])
def query_new():
    """Handles rendering of template from HTMX call to /housing/query_new.
    For the life of me I cannot figure out how to reflect the input name in
    request.form, else I could parse this in `query`. Therefore, this function exists."""
    parsed_params = parse_query_form(request.form)
    posts = list(read_craigslist_housing(parsed_params))
    return render_template(
        "housing/table.html",
        posts=sorted(
            tidy_posts(posts), key=lambda x: datetime.strptime(x["last_updated"], "%Y-%m-%d %H:%M"), reverse=True
        ),
    )


def parse_query_form(request_form):
    params = {key: value.lower() for key, value in request_form.items() if value and value not in ["-"]}
    if params.get("area"):
        params["area"] = SFBAY_AREA_KEY[params["area"]]
    return params


#  ~~~~~~~~~~ BEGIN RESTFUL API ~~~~~~~~~~


@housing.route("/housing/<site>", subdomain="api")
def api_site(site):
    """REST-like API for Craigslist housing - querying with Craigslist site."""
    params = {**{"site": site}, **request.args.to_dict()}
    try:
        return jsonify(list(read_craigslist_housing(params)))
    except ValidationError as e:
        raise InvalidUsage(str(e).capitalize(), status_code=400) from e


@housing.route("/housing/<site>/<area>", subdomain="api")
def api_site_area(site, area):
    """REST-like API for Craigslist housing - querying with Craigslist site
    and area."""
    params = {**{"site": site, "area": area}, **request.args.to_dict()}
    try:
        # Only allow 100 posts to display
        return jsonify(list(read_craigslist_housing(params)))
    except ValidationError as e:
        raise InvalidUsage(str(e).capitalize(), status_code=400) from e


@housing.route("/housing", subdomain="docs")
def api_docs():
    """Documentation page for personal website's API."""
    content = {
        "title": "API Documentation: Housing",
        "profile_img": "me_arrow.png",
        "docs": read_docs(),
    }
    return render_template("housing/docs.html", content=content)
