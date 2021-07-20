SCORE_COLORS = {
    "very-poor": "bg-red-400",
    "poor": "bg-red-300",
    "mild-poor": "bg-red-200",
    "neutral": "bg-white",
    "mild-good": "bg-green-200",
    "good": "bg-green-300",
    "very-good": "bg-green-400",
}


def tidy_post(post):
    post["score_color"] = get_score_color(post["score"])
    return post


def get_score_color(score):
    if score == 0.0:
        return SCORE_COLORS["neutral"]
    if score > 66.7:
        return SCORE_COLORS["very-good"]
    if score > 33.3:
        return SCORE_COLORS["good"]
    if score > 0.0:
        return SCORE_COLORS["mild-good"]
    if score < -66.7:
        return SCORE_COLORS["very-poor"]
    if score < -33.3:
        return SCORE_COLORS["poor"]
    if score < 0.0:
        return SCORE_COLORS["mild-poor"]
