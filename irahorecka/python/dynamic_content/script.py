import os
from dynamic_content import write_github_repos
key = os.environ.get('GitHub')
write_github_repos(key)
