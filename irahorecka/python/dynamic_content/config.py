import os
import yaml
from pathlib import Path


CONFIG_PATH = Path(__file__).absolute().parent.parent.parent.parent / "config.yaml"
with open(CONFIG_PATH, "r") as config:
    GITHUB_REPOS = yaml.safe_load(config)["github-repos"]
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
