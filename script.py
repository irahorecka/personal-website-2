import os
from irahorecka.python.dynamic_content import write_github_repos

key = os.environ.get("GITHUB_TOKEN")
write_github_repos(key)
