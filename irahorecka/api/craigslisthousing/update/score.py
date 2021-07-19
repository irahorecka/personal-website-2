"""
"""

from sqlalchemy.sql import func, and_
import numpy as np

from irahorecka.models import db, CraigslistHousing


def write_craigslist_housing_score(site, areas):
    """ENTRY POINT: Assigns and writes Craigslist housing value scores to every post."""
    # Scoring is ONLY applied to posts with a non-zero ft2 value.
    query_site = CraigslistHousing.query.filter(CraigslistHousing.site == site)
    # For scoring purposes: converts posts with 0 bedrooms to have a traceable bedroom count of 0.99
    query_site.filter(CraigslistHousing.bedrooms == 0).update({CraigslistHousing.bedrooms: 0.99})

    for area in areas:
        data = get_price_per_ft2_db(site, area)
        query_area = CraigslistHousing.query.filter(and_(CraigslistHousing.ft2 != 0, CraigslistHousing.area == area))
        query_area.update({CraigslistHousing.score: calculate_post_score(data, CraigslistHousing)})

    # Reverts posts with 0.99 bedrooms to have its original value of 0
    query_site.filter(CraigslistHousing.bedrooms == 0.99).update({CraigslistHousing.bedrooms: 0})
    normalize_score(query_site, CraigslistHousing)
    db.session.commit()


def calculate_post_score(data, model):
    """Calculates value score for every post. Read description below for calc breakdown:
    - Calculate AVG, STDEV price/sqft for posts within site and area.
        - Area value is multiplied with 0.55 coefficient, Site value with 0.35 coefficient.
        - If a post does not have sqft, give them neutral score (1.0).
    - Score equation:
        = -1 * (0.55 * (1 + (0.55 * stdev_within_area)) + 0.35 * (1 + (0.35 * stdev_within_bayarea)) + 0.1 * (1 + math.log(num_bedrooms)))
    - Purely average model should equate to a score of 1.0, meaning average price within Site, Area, and has 1 bedroom.
    - Score more than 1.0 is GOOD, less than 1.0 is BAD."""
    price_per_ft2 = model.price / model.ft2
    site_std = (price_per_ft2 - data["price_ft2_avg_site"]) / data["price_ft2_std_site"]
    area_std = (price_per_ft2 - data["price_ft2_avg_area"]) / data["price_ft2_std_area"]
    site_weight = 0.35 * (1 + (0.35 * site_std))
    area_weight = 0.55 * (1 + (0.55 * area_std))
    bedroom_weight = 0.1 * func.log(model.bedrooms)

    return -1 * (site_weight + area_weight + bedroom_weight)


def get_price_per_ft2_db(site, area):
    """Gets price/sqft AVG and STDEV within Site and Area locale."""
    price_per_ft2_site = get_price_per_ft2(get_valid_posts(CraigslistHousing).filter(CraigslistHousing.site == site))
    price_per_ft2_area = get_price_per_ft2(get_valid_posts(CraigslistHousing).filter(CraigslistHousing.area == area))
    return {
        "price_ft2_avg_site": round(np.average(price_per_ft2_site), 3),
        "price_ft2_avg_area": round(np.average(price_per_ft2_area), 3),
        "price_ft2_std_site": round(np.std(price_per_ft2_site), 3),
        "price_ft2_std_area": round(np.std(price_per_ft2_area), 3),
    }


def get_price_per_ft2(query):
    """Takes posts within 5% - 95% percentile price/sqft from a given query."""
    ft2, price = get_ft2_price_within_percentile(query, 5, 95)
    return [price[idx] / ft2[idx] for idx in range(len(ft2))]


def get_ft2_price_within_percentile(query, perc_min, perc_max):
    """Takes lower and upper percentile limit and returns a tuple of lists where the ft2
    is within the percentile range. Content of price is directly determined by the curated
    output of ft2."""
    # Trim percentile and get index to bind to price and ft2 values
    ft2, price = map(lambda x: (np.array(x)), zip(*[(post.ft2, post.price) for post in query.all()]))
    low = np.percentile(ft2, perc_min)
    high = np.percentile(ft2, perc_max)
    desired_percentile = np.where(np.logical_and(ft2 >= low, ft2 <= high))
    return (ft2[desired_percentile], price[desired_percentile])


def get_valid_posts(model):
    """Return housing posts where ft2 is greater than 100 and price greater than $300."""
    return model.query.with_entities(model.ft2, model.price, model.area).filter(
        and_(model.ft2 > 100, model.price > 300)
    )


def normalize_score(query, model):
    """Normalizes score to fall within -100 and +100. of what's low and high, respectively."""
    min_norm_score = -100
    max_norm_score = 100
    # Update all model.score value with NoneType to be the average of min and max normalized scores
    query.filter(model.ft2 == 0).update({model.score: (min_norm_score + max_norm_score) / 2})

    # Get query with all numtypes in model.score
    query_num = query.filter(model.score != 0)
    min_q_score, max_q_score = get_min_max_scores(query_num)
    query_num.filter(model.score <= min_q_score).update({model.score: min_norm_score})
    query_num.filter(model.score >= max_q_score).update({model.score: max_norm_score})

    # Get query with model.score within min_q_score and max_q_score
    query_range = query_num.filter(and_(model.score >= min_q_score, model.score <= max_q_score))
    # Equation for normalizing score
    # = (((score - low_score) / (high_score - low_score)) * (2 * max_norm_score)) + min_norm_score
    query_range.update(
        {
            model.score: ((model.score - min_q_score) / (max_q_score - min_q_score)) * (2 * max_norm_score)
            + min_norm_score
        }
    )


def get_min_max_scores(query):
    """To be called after binding score to posts. Normalizes score to more user friendly values.
    See `normalize_score`. Input query where query.score is all numerics."""
    scores = np.array([post.score for post in query.all()])
    # Takes scores within 5% to 95% percentile - sets these as absolute min and max, respectively
    low = np.percentile(scores, 5)
    high = np.percentile(scores, 95)
    return low, high
