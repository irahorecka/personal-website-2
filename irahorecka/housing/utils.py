import json
from pathlib import Path

DOCS_PATH = Path(__file__).absolute().parent.joinpath("docs.json")


SCORE_COLORS = {
    "very-poor": "bg-red-400",
    "poor": "bg-red-300",
    "mild-poor": "bg-red-200",
    "neutral": "bg-white",
    "mild-good": "bg-green-200",
    "good": "bg-green-300",
    "very-good": "bg-green-400",
}


def tidy_posts(posts):
    for post in posts:
        post["score_color"] = get_score_color(post["score"])
    return posts


def get_score_color(score):
    if score == 0.0:
        return SCORE_COLORS["neutral"]
    if score >= 80:
        return SCORE_COLORS["very-good"]
    if score >= 40:
        return SCORE_COLORS["good"]
    if score >= 0.0:
        return SCORE_COLORS["mild-good"]
    if score <= -80:
        return SCORE_COLORS["very-poor"]
    if score <= -40:
        return SCORE_COLORS["poor"]
    if score <= 0.0:
        return SCORE_COLORS["mild-poor"]


def read_docs():
    """Returns `neighborhoods.json` as dictionary."""
    with open(DOCS_PATH) as file:
        docs = json.load(file)
    return docs
