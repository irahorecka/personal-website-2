from irahorecka.models import db, GitHubRepo, RepoLanguage, CraigslistHousing
from irahorecka.python.dynamic_content.config import GITHUB_TOKEN, GITHUB_REPOS
from irahorecka.python.dynamic_content.github_repos import fetch_github_repos
from irahorecka.python.dynamic_content.craigslist_housing import fetch_craigslist_housing


def read_github_repos():
    """Returns GitHub repos information as a dictionary."""
    repos = []
    for repo_name in GITHUB_REPOS:
        repo = GitHubRepo.query.filter_by(name=repo_name).first()
        repos.append(
            {
                "name": str(repo.name),
                "full_name": str(repo.full_name),
                "description": str(repo.description),
                "license": str(repo.license),
                "private": bool(repo.private),
                "stars": int(repo.stars),
                "forks": int(repo.forks),
                "commits": int(repo.commits),
                "open_issues": int(repo.open_issues),
                "languages": [{"name": str(lang.name), "color": str(lang.color)} for lang in repo.languages],
                "url": str(repo.url),
            }
        )
    return repos


def write_github_repos():
    # Drop content in tables - don't bother updating as hard reset for a small
    # table like this is preferable.
    GitHubRepo.query.delete()
    RepoLanguage.query.delete()
    repos = fetch_github_repos(GITHUB_TOKEN)
    for repo in repos:
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


def read_craigslist_housing():
    """Returns SFBay Craigslist Housing information as a dictionary."""
    import json

    with open("sfbay_housing.json") as file:
        data = json.load(file)
    return data


def write_craigslist_housing():
    craigslist_housing = fetch_craigslist_housing()
    from sqlalchemy import exc

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
