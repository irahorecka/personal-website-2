"""
Clean db of junk data
Criteria:
- Posts older than a week of cleaning
- Repeated titles per given neighborhood in database
"""

import datetime

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
