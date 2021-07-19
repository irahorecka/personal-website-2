"""
"""

from datetime import datetime

from cerberus import Validator

from irahorecka.exceptions import ValidationError
from irahorecka.models import CraigslistHousing


def read_craigslist_housing(request_args):
    """Reads and returns SF Bay Area Craigslist Housing posts as a list of dictionaries
    up to the provided limit."""

    def nullify_empty_value(value):
        """Returns None for a non-truthful value (e.g. 0, "", False)."""
        return None if not value else value

    v_status, v_args = validate_request_args(request_args)
    # Raise ValidationError to caller if parsing of request args failed
    if not v_status:
        raise ValidationError(v_args)

    limit = v_args["limit"]
    filtered_housing_query = filter_requests_query(CraigslistHousing, v_args)
    for idx, post in enumerate(filtered_housing_query):
        if idx == limit:
            return
        yield {
            # Metadata
            "id": post.id,
            "repost_of": nullify_empty_value(post.repost_of),
            "last_updated": datetime.strftime(post.last_updated, "%Y-%m-%d %H:%M"),
            "url": post.url,
            # Location
            "site": post.site,
            "area": post.area,
            "neighborhood": nullify_empty_value(post.neighborhood),
            "address": nullify_empty_value(post.address),
            "lat": nullify_empty_value(post.lat),
            "lon": nullify_empty_value(post.lon),
            # Post
            "title": post.title,
            "price": "$" + str(nullify_empty_value(post.price))
            if nullify_empty_value(post.price) is not None
            else None,
            "housing_type": nullify_empty_value(post.housing_type),
            "bedrooms": nullify_empty_value(post.bedrooms),
            "flooring": nullify_empty_value(post.flooring),
            # `is_furnished` and `no_smoking` are booleans - nullify if False; usually indicative of missing data.
            "is_furnished": nullify_empty_value(post.is_furnished),
            "no_smoking": nullify_empty_value(post.no_smoking),
            "ft2": nullify_empty_value(post.ft2),
            "laundry": nullify_empty_value(post.laundry),
            "rent_period": nullify_empty_value(post.rent_period),
            "parking": nullify_empty_value(post.parking),
            "misc": post.misc.split(";"),
            "score": int(post.score),  # Guaranteeing every `post.score` is a numeric
        }


def validate_request_args(request_args):
    """Validate request args for proper data types. Coerce into datatype if initial
    validation passes, other wise send error code and failure message to be displayed
    to client."""
    # Declare schema within function - usually single query, single validation
    # Avoid worrying about performance impact from declaration
    schema = {
        "id": {"type": "integer", "coerce": int, "default": 0},
        # Cast to float then try to validate as integer.
        "limit": {"type": "integer", "coerce": (float, int), "default": 100_000},
        "area": {"type": "string", "default": ""},
        "site": {"type": "string", "default": ""},
        "neighborhood": {"type": "string", "default": ""},
        "housing_type": {"type": "string", "default": ""},
        "laundry": {"type": "string", "default": ""},
        "parking": {"type": "string", "default": ""},
        "min_bedrooms": {"type": "integer", "coerce": (float, int), "default": 0},
        "max_bedrooms": {"type": "integer", "coerce": (float, int), "default": 10},
        "min_ft2": {"type": "integer", "coerce": (float, int), "default": 0},
        "max_ft2": {"type": "integer", "coerce": (float, int), "default": 1_000_000},
        "min_price": {"type": "integer", "coerce": (float, int), "default": 0},
        "max_price": {"type": "integer", "coerce": (float, int), "default": 100_000},
    }
    v = Validator(schema)
    if not v.validate(request_args):
        return (False, v.errors)
    return (True, v.normalized(request_args))


def filter_requests_query(model, validated_args):
    """Returns filtered db.Model.query object to caller, filtered by arguments
    in `validated_args`."""
    if validated_args.get("id"):
        return (model.query.get(validated_args["id"]),)
    query = filter_categorical(model.query, model, validated_args)
    return filter_scalar(query, model, validated_args)


def filter_categorical(query, model, validated_args):
    """Filters categorical attributes of the requests query.
    E.g. `neighborhood=fremont / union city / newark`."""
    categorical_filter = {
        "area": validated_args["area"],
        "site": validated_args["site"],
        "neighborhood": validated_args["neighborhood"],
        "housing_type": validated_args["housing_type"],
        "laundry": validated_args["laundry"],
        "parking": validated_args["parking"],
    }
    for attr, value in categorical_filter.items():
        query = query.filter(getattr(model, attr).like("%%%s%%" % value))
    return query


def filter_scalar(query, model, validated_args):
    """Filters scalar attributes of the requests query.
    E.g. `min_price=1000`."""
    return (
        query.filter(model.bedrooms >= validated_args["min_bedrooms"])
        .filter(model.bedrooms <= validated_args["max_bedrooms"])
        .filter(model.ft2 >= validated_args["min_ft2"])
        .filter(model.ft2 <= validated_args["max_ft2"])
        .filter(model.price >= validated_args["min_price"])
        .filter(model.price <= validated_args["max_price"])
    )
