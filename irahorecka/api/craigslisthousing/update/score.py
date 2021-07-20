"""
"""

import numpy as np
from sqlalchemy.orm import query
from sqlalchemy.sql import func, and_

from irahorecka.models import db, CraigslistHousing


def write_craigslist_housing_score(site, areas):
    """ENTRY POINT: Assigns and writes Craigslist housing value scores to every post."""
    # For scoring purposes: converts posts with 0 bedrooms to have a traceable bedroom count of 0.5
    CraigslistHousing.query.filter(CraigslistHousing.bedrooms == 0).update({CraigslistHousing.bedrooms: 0.5})
    query_site = CraigslistHousing.query.filter(CraigslistHousing.site == site)
    query_site_ft2 = query_site.filter(CraigslistHousing.ft2 != 0)

    for area in areas:
        query_area = query_site.filter(CraigslistHousing.area == area)
        query_area_ft2 = query_area.filter(CraigslistHousing.ft2 != 0)

        # Calculate score for posts with price and ft2
        ft2 = Ft2(CraigslistHousing, query_site_ft2, query_area_ft2)
        ft2.write_score(query_area_ft2)
        normalize_score(query_area_ft2, CraigslistHousing, -100, 100)

        # Calculate score for posts with price without ft2
        bedrooms = Bedrooms(CraigslistHousing, query_site, query_area)
        query_sans_ft2_area = query_area.filter(CraigslistHousing.ft2 == 0)
        bedrooms.write_score(query_sans_ft2_area)
        normalize_score(query_sans_ft2_area, CraigslistHousing, -100, 100)

    # Reverts posts with 0.5 bedrooms to have its original value of 0
    CraigslistHousing.query.filter(CraigslistHousing.bedrooms == 0.5).update({CraigslistHousing.bedrooms: 0})
    db.session.commit()


class Base:
    def __init__(self, model, query_site, query_area):
        self.model = model
        self.query_site = query_site
        self.query_area = query_area

    def _calculate_post_score(self, site_z_score, area_z_score):
        """Calculates value score for every post. Read description below for calc breakdown:
        - Calculate AVG, STDEV price/sqft for posts within site and area.
            - Area value is multiplied with 0.6 coefficient, Site value with 0.3 coefficient.
            - If a post does not have sqft, give them neutral score (1.0).
        - Score equation:
            = 0.6 * (1 - (0.6 * stdev_within_area)) + 0.3 * (1 - (0.3 * stdev_within_bayarea)) + 0.1 * (1 + math.log(num_bedrooms)) - 1
        - Purely average post should equate to a score of 1.0, meaning average price within Site, Area, and has 1 bedroom.
        - Score more than 0 is GOOD, less than 0 is BAD."""
        site_weight = 0.3 * (1 - (0.3 * site_z_score))
        area_weight = 0.6 * (1 - (0.6 * area_z_score))
        bedroom_weight = 0.1 * (1 + func.log(self.model.bedrooms))

        # Subtract 1, which is the neutral score
        return site_weight + area_weight + bedroom_weight - 1

    @staticmethod
    def _get_output_within_percentile(fn, *args, perc_min=5, perc_max=95):
        """Takes lower and upper percentile limit and returns a tuple of lists where the output
        (i.e. fn(arg1, arg2))) is within the specified percentile range."""
        output = fn(*args)
        low = np.percentile(output, perc_min)
        high = np.percentile(output, perc_max)
        desired_percentile = np.where(np.logical_and(output >= low, output <= high))
        return output[desired_percentile]


class Ft2(Base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stats = self._get_sqrt_price_per_ft2_stats()

    def write_score(self, query_write):
        price_per_ft2 = func.sqrt(self.model.price / self.model.ft2)
        site_z_score = (price_per_ft2 - self.stats["sqrt_price_ft2_avg_site"]) / self.stats["sqrt_price_ft2_std_site"]
        area_z_score = (price_per_ft2 - self.stats["sqrt_price_ft2_avg_area"]) / self.stats["sqrt_price_ft2_std_area"]
        query_write.update({self.model.score: self._calculate_post_score(site_z_score, area_z_score)})

    def _get_sqrt_price_per_ft2_stats(self):
        sqrt_price_per_ft2_site = self._get_sqrt_price_per_ft2(self.query_site)
        sqrt_price_per_ft2_area = self._get_sqrt_price_per_ft2(self.query_area)
        return {
            "sqrt_price_ft2_avg_site": np.average(np.square(sqrt_price_per_ft2_site)),
            "sqrt_price_ft2_avg_area": np.average(np.square(sqrt_price_per_ft2_area)),
            "sqrt_price_ft2_std_site": np.std(np.square(sqrt_price_per_ft2_site)),
            "sqrt_price_ft2_std_area": np.std(np.square(sqrt_price_per_ft2_area)),
        }

    def _get_sqrt_price_per_ft2(self, query):
        """Takes posts within 5% - 95% percentile price/sqft from a given query."""
        price, ft2 = map(lambda x: (np.array(x)), zip(*[(post.price, post.ft2) for post in query.all()]))
        # Get an np.array of sqrt(price / ft2) - would love to normalize with log2, but database cannot handle errant log(0) op
        return self._get_output_within_percentile(
            lambda x, y: np.sqrt(np.divide(x, y)), price, ft2, perc_min=5, perc_max=95
        )


class Bedrooms(Base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stats = self._get_sqrt_price_per_bedroom_stats()
        # Penalty value to add to z-score due to post not having ft2 attribute
        self.bdrm_penalty_z_score = 0.2

    def write_score(self, query_write):
        price_per_bedroom = self._sqrt_price_per_bedroom_fn(func.sqrt, func.log, self.model.price, self.model.bedrooms)
        site_z_score = self.bdrm_penalty_z_score + (
            (price_per_bedroom - self.stats["sqrt_price_bedroom_avg_site"]) / self.stats["sqrt_price_bedroom_std_site"]
        )
        area_z_score = self.bdrm_penalty_z_score + (
            (price_per_bedroom - self.stats["sqrt_price_bedroom_avg_area"]) / self.stats["sqrt_price_bedroom_std_area"]
        )
        query_write.update({self.model.score: self._calculate_post_score(site_z_score, area_z_score)})

    def _get_sqrt_price_per_bedroom_stats(self):
        sqrt_price_per_bedroom_site = self._get_sqrt_price_per_bedroom(self.query_site)
        sqrt_price_per_bedroom_area = self._get_sqrt_price_per_bedroom(self.query_area)
        return {
            "sqrt_price_bedroom_avg_site": np.average(sqrt_price_per_bedroom_site),
            "sqrt_price_bedroom_avg_area": np.average(sqrt_price_per_bedroom_area),
            "sqrt_price_bedroom_std_site": np.std(sqrt_price_per_bedroom_site),
            "sqrt_price_bedroom_std_area": np.std(sqrt_price_per_bedroom_area),
        }

    def _get_sqrt_price_per_bedroom(self, query):
        """Takes posts within 5% - 95% percentile price/sqft from a given query."""
        # Max bedrooms allowed is 7
        query = query.filter(self.model.bedrooms < 8)
        price, bedrooms = map(lambda x: (np.array(x)), zip(*[(post.price, post.bedrooms) for post in query.all()]))
        return self._get_output_within_percentile(
            self._sqrt_price_per_bedroom_fn, np.sqrt, np.log, price, bedrooms, perc_min=5, perc_max=95
        )

    @staticmethod
    def _sqrt_price_per_bedroom_fn(sqrt_fn, log_fn, price, bedrooms):
        # Get log2(bedrooms value)
        return sqrt_fn((price + (price * (1 - log_fn(bedrooms)))) / 2)


def normalize_score(query, model, min_score, max_score):
    """Normalizes score to fall within -100 and +100. of what's low and high, respectively."""
    # Update all model.score value with NoneType to be the average of min and max normalized scores
    query.filter(model.score == 0).update({model.score: (min_score + max_score) / 2})

    # Get query with all numtypes in model.score
    query_num = query.filter(model.score != 0)
    min_q_score, max_q_score = get_min_max_scores(query_num)
    query_num.filter(model.score <= min_q_score).update({model.score: min_score})
    query_num.filter(model.score >= max_q_score).update({model.score: max_score})

    # Get query with model.score within min_q_score and max_q_score
    query_range = query_num.filter(and_(model.score >= min_q_score, model.score <= max_q_score))
    # Equation for normalizing score
    # = (((score - low_score) / (high_score - low_score)) * (2 * max_score)) + min_score
    normalized_score = ((model.score - min_q_score) / (max_q_score - min_q_score)) * (2 * max_score) + min_score
    # Round normalized score to the nearest 5
    query_range.update({model.score: func.round(normalized_score * 0.2) / 0.2})


def get_min_max_scores(query):
    """To be called after binding score to posts. Normalizes score to more user friendly values.
    See `normalize_score`. Input query where query.score is all numerics."""
    scores = np.array([post.score for post in query.all()])
    # Takes scores within 1% to 99% percentile - sets these as absolute min and max, respectively
    low = np.percentile(scores, 1)
    high = np.percentile(scores, 99)
    return low, high
