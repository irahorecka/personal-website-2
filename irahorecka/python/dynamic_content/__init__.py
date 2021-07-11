from irahorecka.models import db, GitHubRepo, RepoLanguage
from irahorecka.python.dynamic_content.config import GITHUB_TOKEN, GITHUB_REPOS
from irahorecka.python.dynamic_content.github_repos import fetch_github_repos


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
        repo_session = GitHubRepo(
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
        db.session.add(repo_session)
        for lang in repo["languages"]:
            # Back-reference language used in repository to `repo_session`
            lang_session = RepoLanguage(name=lang["name"], color=lang["color"], repo=repo_session)
            db.session.add(lang_session)
    db.session.commit()


def read_craigslist_housing():
    """Returns SFBay Craigslist Housing information as a dictionary."""
    pass
