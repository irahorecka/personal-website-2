"""
This module will gather almost every sf bay area housing posts and write to a json file
This module will then have options to:
    1. return all posts in json format
    2. return posts queried against json format
Get zip codes for alameda, contra costa, santa clara, san francisco, santa cruz, sonoma, and san mateo

NOTE: eventually, we want to transition data storage and fetching from a database
"""

import pycraigslist
from pycraigslist.exceptions import MaximumRequestsError
from sqlalchemy import exc

from irahorecka.models import db, CraigslistHousing


def read_craigslist_housing(requests_args):
    """Reads and returns SF Bay Area Craigslist Housing posts as a list of dictionaries."""
    filtered_housing_query = filter_requests_query(CraigslistHousing, requests_args)
    # Read up to 1,000,000 items if no limit filter is provided.
    limit = requests_args.get("limit", 1_000_000)
    for idx, post in enumerate(filtered_housing_query):
        if idx == limit:
            return
        yield {
            "country": post.country,
            "region": post.region,
            "site": post.site,
            "area": post.area,
            "post_id": post.post_id,
            "repost_of": post.repost_of,
            "last_updated": post.last_updated,
            "title": post.title,
            "neighborhood": post.neighborhood,
            "address": post.address,
            "lat": post.lat,
            "lon": post.lon,
            "price": post.price,
            "bedrooms": post.bedrooms,
            "housing_type": post.housing_type,
            "area_ft2": post.area_ft2,
            "laundry": post.laundry,
            "parking": post.parking,
            "url": post.url,
            "misc": post.misc.split(";"),
        }


def filter_requests_query(session, requests_args):
    """Returns filtered db.Model.query object to caller, filtered by arguments
    in `requests_args`."""
    query_filter = {
        "post_id": requests_args.get("post_id", ""),
        "area": requests_args.get("area", ""),
        "neighborhood": requests_args.get("neighborhood", ""),
        "bedrooms": requests_args.get("bedrooms", ""),
        "housing_type": requests_args.get("housing_type", ""),
        "laundry": requests_args.get("laundry", ""),
        "parking": requests_args.get("parking", ""),
    }
    query = session.query
    for attr, value in query_filter.items():
        query = query.filter(getattr(session, attr).like("%%%s%%" % value))
    return query


def write_craigslist_housing(site, areas=["null"]):
    """Writes unique SF Bay Area Craigslist Housing posts (`apa`) to database."""
    craigslist_housing = fetch_craigslist_apa(site, areas)
    posts = [
        CraigslistHousing(
            id=post["id"],
            country=post.get("country", ""),
            region=post.get("region", ""),
            site=post.get("site", ""),
            area=post.get("area", ""),
            post_id=post["id"],
            repost_of=post.get("repost_of", ""),
            last_updated=post.get("last_updated", ""),
            title=post.get("title", ""),
            neighborhood=post.get("neighborhood", ""),
            address=post.get("address", ""),
            lat=post.get("lat", ""),
            lon=post.get("lon", ""),
            price=post.get("price", ""),
            bedrooms=post.get("bedrooms", ""),
            housing_type=post.get("housing_type", ""),
            area_ft2=post.get("area-ft2", ""),
            laundry=post.get("laundry", ""),
            parking=post.get("parking", ""),
            url=post.get("url", ""),
            misc=";".join(post.get("misc", [])),
        )
        for post in craigslist_housing
    ]
    try:
        db.session.add_all(posts)
        db.session.commit()
    except exc.IntegrityError:
        db.session.rollback()


def fetch_craigslist_apa(*args, **kwargs):
    """Fetches Craigslist apartments / housing posts."""
    posts = []
    post_id_ref = set()
    for apa in yield_apa(*args, **kwargs):
        for post in apa.search_detail():
            post_id = int(post["id"])
            # Performs checks to ensure no duplication of posts in database.
            if post_id in post_id_ref or CraigslistHousing.query.get(post_id):
                continue
            post_id_ref.add(post_id)
            posts.append(post)
            # Don't add to database here, we want to writing to database executed ASAP.
            # i.e. no unnecessary write latency during Craigslist scraping.
    return posts


def yield_apa(site, areas):
    """Yields detailed posts from pycraigslist.housing.apa instances."""
    # Query pycraigslist instances even if there's a connection error.
    while True:
        try:
            yield from [
                pycraigslist.housing.apa(site=site, area=area, filters=query_filter)
                for area in areas
                for query_filter in yield_apa_filters()
            ]
            return
        except MaximumRequestsError:
            pass


def yield_apa_filters():
    """Yields apa filters for caller queries."""
    # Only filter for prices, ranging from $0 - $8000 in $500 increments to gain more listing coverage.
    # Craigslist limits number of posts to 3000 for any given query.
    yield from [
        {"min_price": min_price, "max_price": max_price}
        for min_price, max_price in zip(range(0, 8000, 500), range(500, 8500, 500))
    ]
