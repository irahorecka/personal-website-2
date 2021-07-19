"""
"""

from sqlalchemy.sql import func, and_
import numpy as np

from irahorecka.models import db, CraigslistHousing


def write_craigslist_housing_score(site, areas):
    """ENTRY POINT: Assigns and writes Craigslist housing value scores to every post."""
    # Scoring is ONLY applied to posts with a non-zero ft2 value.
    # TODO: FILTER OUT PRICES THAT ARE BELOW 300 UP HERE
    query_site = CraigslistHousing.query.filter(CraigslistHousing.site == site)
    # For scoring purposes: converts posts with 0 bedrooms to have a traceable bedroom count of 0.99
    query_site.filter(CraigslistHousing.bedrooms == 0).update({CraigslistHousing.bedrooms: 0.99})

    for area in areas:

        query_ft2_area = CraigslistHousing.query.filter(
            and_(CraigslistHousing.ft2 != 0, CraigslistHousing.area == area)
        )
        data = get_price_per_ft2_db(CraigslistHousing, query_ft2_area, site, area)
        site_std, area_std = get_stds_price_ft2(CraigslistHousing, data)
        query_ft2_area.update({CraigslistHousing.score: calculate_post_score(CraigslistHousing, site_std, area_std)})

        query_sans_ft2_area = CraigslistHousing.query.filter(
            and_(CraigslistHousing.ft2 == 0, CraigslistHousing.area == area)
        )
        data = get_price_per_bdrm_db(CraigslistHousing, query_sans_ft2_area, site, area)
        site_std, area_std = get_stds_sans_price_bdrm(CraigslistHousing, data)
        query_sans_ft2_area.update(
            {CraigslistHousing.score: calculate_post_score(CraigslistHousing, site_std, area_std)}
        )

    # Reverts posts with 0.99 bedrooms to have its original value of 0
    query_site.filter(CraigslistHousing.bedrooms == 0.99).update({CraigslistHousing.bedrooms: 0})
    normalize_score(query_site, CraigslistHousing)
    db.session.commit()


def calculate_post_score(model, site_std, area_std):
    """Calculates value score for every post. Read description below for calc breakdown:
    - Calculate AVG, STDEV price/sqft for posts within site and area.
        - Area value is multiplied with 0.55 coefficient, Site value with 0.35 coefficient.
        - If a post does not have sqft, give them neutral score (1.0).
    - Score equation:
        = -1 * (0.55 * (1 + (0.55 * stdev_within_area)) + 0.35 * (1 + (0.35 * stdev_within_bayarea)) + 0.1 * (1 + math.log(num_bedrooms)))
    - Purely average model should equate to a score of 1.0, meaning average price within Site, Area, and has 1 bedroom.
    - Score more than 1.0 is GOOD, less than 1.0 is BAD."""
    site_weight = 0.35 * (1 + (0.35 * site_std))
    area_weight = 0.55 * (1 + (0.55 * area_std))
    bedroom_weight = 0.1 * (1 + func.log(model.bedrooms))

    return -1 * (site_weight + area_weight + bedroom_weight)


def get_stds_price_ft2(model, data):
    price_per_ft2 = model.price / model.ft2
    site_std = (price_per_ft2 - data["price_ft2_avg_site"]) / data["price_ft2_std_site"]
    area_std = (price_per_ft2 - data["price_ft2_avg_area"]) / data["price_ft2_std_area"]
    return site_std, area_std


def get_stds_sans_price_bdrm(model, data):
    # Calculate score value for posts without ft2 -- accomplish this through using bedrooms
    price_per_bdrm = model.price / model.bedrooms
    # 1.2 coefficient is natural penalty for not having ft2, which is a better evaluator of value
    site_std = 1.2 * (price_per_bdrm - data["price_bdrm_avg_site"]) / data["price_bdrm_std_site"]
    area_std = 1.2 * (price_per_bdrm - data["price_bdrm_avg_area"]) / data["price_bdrm_std_area"]
    return site_std, area_std


def get_price_per_ft2_db(model, query, site, area):
    """Gets price/sqft AVG and STDEV within Site and Area locale."""
    price_per_ft2_site = get_price_per_ft2(get_valid_posts(model, query).filter(model.site == site))
    price_per_ft2_area = get_price_per_ft2(get_valid_posts(model, query).filter(model.area == area))
    return {
        "price_ft2_avg_site": round(np.average(price_per_ft2_site), 3),
        "price_ft2_avg_area": round(np.average(price_per_ft2_area), 3),
        "price_ft2_std_site": round(np.std(price_per_ft2_site), 3),
        "price_ft2_std_area": round(np.std(price_per_ft2_area), 3),
    }


def get_price_per_bdrm_db(model, query, site, area):
    """Gets price/sqft AVG and STDEV within Site and Area locale."""
    price_per_bdrm_site = get_price_per_bdrm(get_valid_posts(model, query).filter(model.site == site))
    price_per_bdrm_area = get_price_per_bdrm(get_valid_posts(model, query).filter(model.area == area))
    return {
        "price_bdrm_avg_site": round(np.average(price_per_bdrm_site), 3),
        "price_bdrm_avg_area": round(np.average(price_per_bdrm_area), 3),
        "price_bdrm_std_site": round(np.std(price_per_bdrm_site), 3),
        "price_bdrm_std_area": round(np.std(price_per_bdrm_area), 3),
    }


def get_valid_posts(model, query):
    """Return housing posts where price greater than $300."""
    return query.with_entities(model.bedrooms, model.ft2, model.price, model.area).filter(model.price > 300)


def get_price_per_bdrm(query):
    """Takes posts within 5% - 95% percentile price/sqft from a given query."""
    bedrooms, price = map(lambda x: (np.array(x)), zip(*[(post.bedrooms, post.price) for post in query.all()]))
    return get_quotient_within_percentile(price, bedrooms, 5, 95)


def get_price_per_ft2(query):
    """Takes posts within 5% - 95% percentile price/sqft from a given query."""
    ft2, price = map(lambda x: (np.array(x)), zip(*[(post.ft2, post.price) for post in query.all()]))
    return get_quotient_within_percentile(price, ft2, 5, 95)


def get_quotient_within_percentile(num, den, perc_min, perc_max):
    """Takes lower and upper percentile limit and returns a tuple of lists where the quotient
    (i.e. numerator / denominator) is within specified percentile range."""
    quotient = np.divide(num, den)
    low = np.percentile(quotient, perc_min)
    high = np.percentile(quotient, perc_max)
    desired_percentile = np.where(np.logical_and(quotient >= low, quotient <= high))
    return quotient[desired_percentile]


def normalize_score(query, model):
    """Normalizes score to fall within -100 and +100. of what's low and high, respectively."""
    min_norm_score = -100
    max_norm_score = 100
    # Update all model.score value with NoneType to be the average of min and max normalized scores
    query.filter(model.score == 0).update({model.score: (min_norm_score + max_norm_score) / 2})

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
