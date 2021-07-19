"""
"""

from datetime import datetime

import pycraigslist
from pycraigslist.exceptions import MaximumRequestsError
from sqlalchemy import exc

from irahorecka.models import db, CraigslistHousing


def write_craigslist_housing(site, areas=("null",)):
    """Writes unique SF Bay Area Craigslist Housing posts (`apa`) to database."""
    craigslist_housing = fetch_craigslist_apa(site, areas)
    posts = [
        CraigslistHousing(
            id=post["id"],
            site=post.get("site", ""),
            area=post.get("area", "0"),
            repost_of=post.get("repost_of", ""),
            last_updated=datetime.strptime(post["last_updated"], "%Y-%m-%d %H:%M"),
            title=post.get("title", ""),
            neighborhood=post.get("neighborhood", ""),
            address=post.get("address", ""),
            # Coordinates for Guest Peninsula, Antactica if there's no lat or lon.
            lat="-76.299965" if not post.get("lat") else post["lat"],
            lon="-148.003021" if not post.get("lon") else post["lon"],
            # Convert price into numerics: e.g. '$1,500' --> '1500'
            price=post.get("price", "0").replace("$", "").replace(",", ""),
            housing_type=post.get("housing_type", ""),
            bedrooms=post.get("bedrooms", "0"),
            flooring=post.get("flooring", ""),
            is_furnished=False if post.get("is_furnished", "false") == "false" else True,
            no_smoking=False if post.get("no_smoking", "false") == "false" else True,
            ft2=post.get("area-ft2", "0"),
            laundry=post.get("laundry", ""),
            parking=post.get("parking", ""),
            rent_period=post.get("rent_period", ""),
            url=post.get("url", ""),
            misc=";".join(post.get("misc", [])),
            _title_neighborhood=f'{post.get("neighborhood", "")}{post.get("title", "")}',
        )
        for post in craigslist_housing
    ]
    try:
        db.session.add_all(posts)
        db.session.commit()
    except exc.IntegrityError as e:
        print(e)
        db.session.rollback()


def fetch_craigslist_apa(*args, **kwargs):
    """Fetches Craigslist apartments / housing posts."""
    posts = []
    post_id_ref = set()
    for apa in yield_apa(*args, **kwargs):
        for post in apa.search_detail():
            post_id = int(post["id"])
            # Performs checks to ensure no duplication of post id in current search and CraigslistHousing table.
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
        # for min_price, max_price in ((100, 1500),)
    ]
