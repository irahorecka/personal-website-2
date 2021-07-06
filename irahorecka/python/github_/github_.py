"""
GOAL: Create a JSON format file for useful information regarding your github - use this to make a nice github summary webpage
    Create a RESTful API to query this json content from a separate server (which gathers github information nightly)
    Project this JSON on the front end. Simple query to server to just get the JSON back. 1 request 1 response

JSON content:
    project
        project desc (description)
        stargazer_count
        forks_count
        commit no. (get_commits)
        open_issues_count
        is private (private)
        num collaborators (get_collaborators)
        get_license
"""

import concurrent.futures
import json
import os

from github import Github
from github.GithubException import RateLimitExceededException, UnknownObjectException

JSON_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out.json")
LANGUAGE_COLOR = {
    "python": "#3672a5",
    "css": "#563d7c",
    "html": "#e34c26",
    "javascript": "#f1e05a",
    "makefile": "#427819",
    "c++": "#f34b7d",
    "jupyter notebook": "#da5b0b",
    "r": "#198ce7",
    "ruby": "#701516",
    "swift": "#ffac44",
    "racket": "#3d5caa",
    "rich text format": "#f6f8fa",
    "shell": "#89e051",
    "batchfile": "#c1f12e",
}


def write_repos(access_token):
    """Entry point function to write GitHub user's repos (via access token)
    to `JSON_PATH`. Returns exit code 0 if success, 1 if failure."""
    try:
        user = Github(access_token).get_user()
    except RateLimitExceededException:
        # Throttled access to GitHub's API
        return 1
    repos = user.get_repos()
    project_json = build_repos_json(repos)
    write_json(project_json, JSON_PATH)
    return 0


def build_repos_json(repos):
    """Get projects' name and information as a dictionary."""
    return list(map_threads(build_repo_json, repos))


def map_threads(func, _iterable):
    """Map function with iterable object in using thread pools."""
    with concurrent.futures.ThreadPoolExecutor() as executor:
        result = executor.map(func, _iterable)
    return result


def build_repo_json(repo):
    return {
        "name": repo.full_name.split("/")[-1],
        "full_name": repo.full_name,
        "description": repo.description,
        "license": validate_gh_method(repo.get_license).license.name
        if validate_gh_method(repo.get_license) != ""
        else "",
        "private": repo.private,
        "stars": repo.stargazers_count,
        "forks": repo.forks_count,
        "commits": len(list(validate_gh_method(repo.get_commits))),
        "open_issues": repo.open_issues_count,
        "languages": validate_gh_method(get_languages, repo) if validate_gh_method(get_languages, repo) != "" else "",
        "url": f"https://github.com/{repo.full_name}",
    }


def validate_gh_method(method, *args, **kwargs):
    try:
        return method(*args, **kwargs)
    except UnknownObjectException:
        return ""


def get_languages(repo):
    """Returns language color as seen on GitHub."""
    languages = repo.get_languages()
    return [{"name": lang, "color": LANGUAGE_COLOR.get(lang.lower(), "#ffffff")} for lang in languages]


def write_json(data, output_path):
    """Writes dictionary to JSON file."""
    with open(output_path, "w") as file:
        json.dump(data, file)
