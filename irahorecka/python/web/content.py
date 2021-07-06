from datetime import datetime


def get_age():
    """Gets my age in years."""
    return int(divmod((datetime.now() - datetime(1994, 5, 10)).total_seconds(), 31536000)[0])


CONTENT = {
    "home": {
        "header": "Ira Horecka",
        "content": "Lab Automation Engineer and programming enthusiast.",
    },
    "api": {
        "header": "API time",
        "content": "I enjoy writing API wrappers in Python. Take a look at my REST API for Craigslist housing in the SF Bay Area.",
    },
    "projects": {
        "header": "Programming projects",
        "content": "I'm a self-taught programmer and I really dig it! I am most comfortable with Python and web programming (HTML/CSS/JS).",
    },
    "about": {
        "header": "About me",
        "content": f"Hello, I'm Ira. I'm {get_age()} and will study at the University of Toronto in Fall 2021.",
    },
}


def get_header(key):
    """Gets header value from `content` given a valid key."""
    return CONTENT[key]["header"]


def get_content(key):
    """Gets content value from `content` given a valid key."""
    return CONTENT[key]["content"]
