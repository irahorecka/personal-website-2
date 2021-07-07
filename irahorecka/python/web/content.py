from datetime import datetime


def _get_age():
    """Gets my age in years."""
    return int(divmod((datetime.now() - datetime(1994, 5, 10)).total_seconds(), 31536000)[0])


CONTENT = {
    "home": {
        "header": {"first": "Ira Horecka"},
        "body": {"first": "Lab Automation Engineer and programming enthusiast."},
    },
    "api": {
        "header": {"first": "API time"},
        "body": {
            "first": "I enjoy writing API wrappers in Python. Take a look at my REST API for Craigslist housing in the SF Bay Area."
        },
    },
    "projects": {
        "header": {"first": "Programming projects"},
        "body": {
            "first": "I'm a self-taught programmer and I really dig it! I am most comfortable with Python and web programming (HTML/CSS/JS)."
        },
    },
    "about": {
        "header": {"first": "About me"},
        "body": {
            "first": f"Hello, I'm Ira. I'm {_get_age()} and will study at the University of Toronto in Fall 2021."
        },
    },
}


def get_header(key):
    """Gets header value from `content` given a valid key."""
    return CONTENT[key]["header"]


def get_body(key):
    """Gets body value from `body` given a valid key."""
    return CONTENT[key]["body"]
