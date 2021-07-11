from sqlalchemy import exc

from irahorecka.models import db, GitHubRepo, RepoLanguage, CraigslistHousing
from irahorecka.python.content.config import GITHUB_TOKEN, GITHUB_REPOS
from irahorecka.python.content.dynamic.github_repos import fetch_repos
from irahorecka.python.content.dynamic.craigslist_housing import fetch_sfbay_housing


def read_github_repos():
    """Returns GitHub repos information as a dictionary."""
    for repo_name in GITHUB_REPOS:
        repo = GitHubRepo.query.filter_by(name=repo_name).first()
        yield {
            "name": repo.name,
            "full_name": repo.full_name,
            "description": repo.description,
            "license": repo.license,
            "private": repo.private,
            "stars": repo.stars,
            "forks": repo.forks,
            "commits": repo.commits,
            "open_issues": repo.open_issues,
            "languages": [{"name": lang.name, "color": lang.color} for lang in repo.languages],
            "url": repo.url,
        }


def write_github_repos():
    """Write GitHub repos to database."""
    # Drop content in tables - don't bother updating as hard reset for a small
    # table like this is preferable.
    GitHubRepo.query.delete()
    RepoLanguage.query.delete()
    for repo in fetch_repos(GITHUB_TOKEN):
        repo_entry = GitHubRepo(
            name=repo["name"],
            full_name=repo["full_name"],
            description=repo["description"],
            license=repo["license"],
            private=repo["private"],
            stars=repo["stars"],
            forks=repo["forks"],
            commits=repo["commits"],
            open_issues=repo["open_issues"],
            url=repo["url"],
        )
        db.session.add(repo_entry)
        for lang in repo["languages"]:
            # Back-reference language used in repository to `repo_entry`
            lang_session = RepoLanguage(name=lang["name"], color=lang["color"], repo=repo_entry)
            db.session.add(lang_session)
    db.session.commit()


def read_craigslist_housing(limit=1_000_000):
    """Returns SFBay Craigslist Housing information as a list of dictionaries."""
    for idx, post in enumerate(CraigslistHousing.query):
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


def write_craigslist_housing():
    """Write unique SF Bay Area Craigslist Housing posts (`apa`) to database."""
    craigslist_housing = fetch_sfbay_housing()
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
