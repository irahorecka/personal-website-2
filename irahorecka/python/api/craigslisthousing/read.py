"""
"""

from irahorecka.models import CraigslistHousing


def read_craigslist_housing(requests_args):
    """Reads and returns SF Bay Area Craigslist Housing posts as a list of dictionaries."""

    def nullify_empty_value(value):
        """Returns None for a non-truthful value (e.g. 0, "", False)."""
        return None if not value else value

    filtered_housing_query = filter_requests_query(CraigslistHousing, requests_args)
    # Read up to 1,000,000 items if no limit filter is provided.
    limit = int(requests_args.get("limit", "1_000_000"))
    for idx, post in enumerate(filtered_housing_query):
        if idx == limit:
            return
        yield {
            # Metadata
            "id": post.id,
            "repost_of": nullify_empty_value(post.repost_of),
            "last_updated": nullify_empty_value(post.last_updated),
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
        }


def filter_requests_query(session, requests_args):
    """Returns filtered db.Model.query object to caller, filtered by arguments
    in `requests_args`."""
    query = filter_categorical(session, requests_args)
    return filter_scalar(session, query, requests_args)


def filter_categorical(session, requests_args):
    """Filters categorical attributes of the requests query.
    E.g. `neighborhood=fremont / union city / newark`."""
    categorical_filter = {
        # ID could be queried faster using session.query.get(id), but let's make it simple
        # and it's not a demanding query parameter.
        "id": requests_args.get("id", ""),
        "area": requests_args.get("area", ""),
        "site": requests_args.get("site", ""),
        "neighborhood": requests_args.get("neighborhood", ""),
        "housing_type": requests_args.get("housing_type", ""),
        "bedrooms": requests_args.get("bedrooms", ""),
        "laundry": requests_args.get("laundry", ""),
        "parking": requests_args.get("parking", ""),
    }
    query = session.query
    for attr, value in categorical_filter.items():
        query = query.filter(getattr(session, attr).like("%%%s%%" % value))
    return query


def filter_scalar(session, query, requests_args):
    """Filters scalar attributes of the requests query.
    E.g. `min_price=1000`."""
    scalar_filter = {
        "min_bedrooms": float(requests_args.get("min_bedrooms", "0")),
        "max_bedrooms": float(requests_args.get("max_bedrooms", "100")),
        "min_ft2": float(requests_args.get("min_ft2", "0")),
        "max_ft2": float(requests_args.get("max_ft2", "1000000")),
        "min_price": float(requests_args.get("min_price", "0")),
        "max_price": float(requests_args.get("max_price", "100000")),
    }
    return (
        query.filter(session.bedrooms >= scalar_filter["min_bedrooms"])
        .filter(session.bedrooms <= scalar_filter["max_bedrooms"])
        .filter(session.ft2 >= scalar_filter["min_ft2"])
        .filter(session.ft2 <= scalar_filter["max_ft2"])
        .filter(session.price >= scalar_filter["min_price"])
        .filter(session.price <= scalar_filter["max_price"])
    )
