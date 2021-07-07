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
import yaml
from pathlib import Path

from github import Github
from github.GithubException import RateLimitExceededException, UnknownObjectException


CONFIG_PATH = Path(__file__).absolute().parent.parent.parent.parent.joinpath("config.yaml")
with open(CONFIG_PATH, "r") as config:
    CONFIG_GITHUB = yaml.safe_load(config)["github"]
JSON_PATH = Path(__file__).absolute().parent.joinpath("out.json")
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
    repos_dict = {repo["name"]: repo for repo in map_threads(build_repo_dict, repos) if repo is not None}
    # Sort `repos_dict` in order as it would appear in `CONFIG_GITHUB["repos"]`
    index_map = {repo_name: idx for idx, repo_name in enumerate(CONFIG_GITHUB["repos"])}
    # Build and write a list of repositories to JSON
    repos_list = [tup[1] for tup in sorted(repos_dict.items(), key=lambda pair: index_map[pair[0]])]
    write_json(repos_list, JSON_PATH)
    return 0


def map_threads(func, _iterable):
    """Map function with iterable object in using thread pools."""
    with concurrent.futures.ThreadPoolExecutor() as executor:
        result = executor.map(func, _iterable)
    return result


def build_repo_dict(repo):
    """Isolates desired properties of a GitHub repository."""
    repo_name = repo.full_name.split("/")[-1]
    if repo_name not in CONFIG_GITHUB["repos"]:
        return None
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
    """Wrapper that will return an empty string if PyGithub method
    raises an exception."""
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
