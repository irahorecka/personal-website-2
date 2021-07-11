"""
This module will gather almost every sf bay area housing posts and write to a json file
This module will then have options to:
    1. return all posts in json format
    2. return posts queried against json format
Get zip codes for alameda, contra costa, santa clara, san francisco, santa cruz, sonoma, and san mateo

NOTE: eventually, we want to transition data storage and fetching from a database
"""

import pycraigslist

from irahorecka.models import CraigslistHousing


def yield_apa_filters():
    # Get apa filters for subsequent queries
    # Only filter for prices, ranging from $0 - $8000 in $500 increments to gain more post coverage
    # NOTE: Craigslist limits number of posts to 3000 for any given query
    yield from [
        {"min_price": min_price, "max_price": max_price}
        for min_price, max_price in zip(range(0, 8000, 500), range(500, 8500, 500))
    ]


def yield_sfbay_apa():
    sfbay_areas = ["eby", "nby", "sby", "sfc", "pen", "scz"]
    yield from [
        pycraigslist.housing.apa(site="sfbay", area=area, filters=query_filter)
        for area in sfbay_areas
        for query_filter in yield_apa_filters()
    ]


def fetch_sfbay_housing():
    sfbay_housing = []
    post_id_ref = []
    for apa in yield_sfbay_apa():
        for post in apa.search_detail():
            post_id = int(post["id"])
            # Performs checks to ensure no duplication of posts in database
            if post_id in post_id_ref or CraigslistHousing.query.get(post_id):
                continue
            post_id_ref.append(post_id)
            sfbay_housing.append(post)

    return sfbay_housing
