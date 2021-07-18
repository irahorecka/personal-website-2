"""
Clean db of junk data
Criteria:
- Posts older than a week of cleaning
- Repeated titles per given neighborhood in database
"""

import datetime
import math

import numpy as np

from irahorecka.models import db, CraigslistHousing


def clean_craigslist_housing():
    # Entry point function to clean database - tack on more functions as you see fit
    rm_old_posts(CraigslistHousing)
    rm_duplicate_posts(CraigslistHousing)


def rm_old_posts(model, days=7):
    # Remove posts where `model.last_updated` is over 7 days old
    datetime_threshold = datetime.datetime.now() - datetime.timedelta(days=days)
    model.query.filter(model.last_updated < datetime_threshold).delete()
    db.session.commit()


def rm_duplicate_posts(model):
    # Filter id's where `model._title_neighborhood` is unique
    query = model.query.with_entities(model.id).group_by(model._title_neighborhood)
    del_query = model.__table__.delete().where(model.id.not_in(query))
    # Delete duplicate posts
    db.session.execute(del_query)
    db.session.commit()


def calculate_post_score(post):
    # Take 0.05 - 0.95 percentile usd/sqft all of bay area
    # Take 0.05 - 0.95 percentile usd/sqft within area
    # Calculate avg, stdDEV for both, area value has 0.55 weight, all bay area has 0.35 rate
    # Use this for every post evaluation - if not sqft, give them neutral score
    # 0.55 * (1 + (0.55 * stdev_area)) + 0.35 * (1 + (0.35 * stdev_bayarea)) + 0.1 * (1 + math.log(num_bedrooms))
    # NOTE - purely average post should equate to a score of 1, meaning avg price in bay area, area, and 1 bedroom
    # LESS THAN 1, GOOD : MORE THAN 1, BAD
    data = get_price_per_ft2_db(post["area"])
    price_per_ft2 = post["price"] / post["ft2"]
    site_std = (price_per_ft2 - data["price_ft2_avg_site"]) / data["price_ft2_std_site"]
    area_std = (price_per_ft2 - data["price_ft2_avg_area"]) / data["price_ft2_std_area"]
    site_weight = 0.35 * (1 + (0.35 * site_std))
    area_weight = 0.55 * (1 + (0.55 * area_std))
    bedroom_weight = 0.1 * (1 - math.log(post["bedrooms"]))
    return site_weight + area_weight + bedroom_weight


def get_price_per_ft2_db(area):
    price_per_ft2_site = get_price_per_ft2(get_valid_posts(CraigslistHousing))
    price_per_ft2_area = get_price_per_ft2(get_valid_posts(CraigslistHousing).filter(CraigslistHousing.area == area))
    return {
        "price_ft2_avg_site": round(np.average(price_per_ft2_site), 3),
        "price_ft2_avg_area": round(np.average(price_per_ft2_area), 3),
        "price_ft2_std_site": round(np.std(price_per_ft2_site), 3),
        "price_ft2_std_area": round(np.std(price_per_ft2_area), 3),
    }


def get_price_per_ft2(query):
    ft2, price = get_ft2_price_within_percentile(query, 5, 95)
    return [price[idx] / ft2[idx] for idx in range(len(ft2))]


def get_ft2_price_within_percentile(query, perc_min, perc_max):
    # Trim percentile and get index to bind to price and ft2 values
    ft2, price = map(lambda x: (np.array(x)), zip(*[(post.ft2, post.price) for post in query.all()]))
    low = np.percentile(ft2, perc_min)
    high = np.percentile(ft2, perc_max)
    desired_percentile = np.where(np.logical_and(ft2 >= low, ft2 <= high))
    return (ft2[desired_percentile], price[desired_percentile])


def get_valid_posts(model):
    return model.query.with_entities(model.ft2, model.price, model.area).filter(model.ft2.isnot(0) & model.ft2.isnot(0))
