"""
"""

from pathlib import Path

GALLERY_PATH = Path(__file__).absolute().parent.parent.parent / "static" / "images" / "gallery"
CONTENT = {
    "home": {
        "header": {
            "first": "Ira Horecka",
            "second": "About me",
            "third": "Do I step away from my computer?",
        },
        "body": {
            "first": "Hello, I'm Ira. I enjoy computer programming and will join a PhD program at the University of Toronto to study computational biology.",
            "second": "I live in Mountain View, CA and work as a lab automation engineer at a biotech firm. My educational background is in biochemistry & molecular biology. I started programming almost 3 years ago and have enjoyed it since.",
            "third": 'There was a period in time when I worked as a research associate (RA). I wondered, "How do I break out of the RA title? Did I study a rigorous curriculum to become adept at pipetting?" Before I delve further, I do not intend to undermine RAs, as the career is fulfilling in its own light.',
            "fourth": "My twin brother, who is a software engineer, encouraged me to take up programming, so I did. I improved my skillset and eventually transitioned into an engineering career. I strive to go beyond programming liquid handlers, which is why I'm pursuing a higher education in computational biology - to merge my academic background with my passion in software development.",
            "fifth": "Yes! I enjoy refurbishing bicycles and bass fishing when I'm away from my computer. These hobbies are frustrating and fulfilling, which is a common emotional elixir in any activity with a learning curve; and when things go according to plan, the world is briefly wonderful.",
        },
    },
    "api": {
        "header": {"first": "Housing"},
        "body": {
            "first": "Finding housing on Craigslist is painful. That's why I made this little tool to help you find the best housing deals for your next move.",
            "second": "The current scope is in the San Francisco Bay Area. Let me know if you'd like to see a new location. 🏘️",
        },
    },
    "api_docs": {
        "header": {"first": "API Documentation"},
        "body": {
            "first": "Please review closely for building a structured query. Currently, the only API hosted is for Craigslist Housing in the San Francisco Bay Area."
        },
    },
    "projects": {
        "header": {"first": "Programming projects"},
        "body": {
            "first": "I'm a self-taught programmer and I dig it. I'm most comfortable with Python and web programming (HTML/CSS/JS)."
        },
    },
}


def get_header_text(key):
    """Gets header value from `content` given a valid key."""
    return CONTENT[key]["header"]


def get_body_text(key):
    """Gets body value from `body` given a valid key."""
    return CONTENT[key]["body"]


def get_gallery_imgs():
    """Returns JPEG and PNG filenames in irahorecka/static/images/gallery to caller."""
    # Note: all images in irahorecka/static/images/gallery must be jpeg or png filetypes
    glob_imgs = [list(GALLERY_PATH.glob(ext)) for ext in ("*.png", "*.PNG", "*.jpeg", "*.JPEG", "*.jpg", "*.JPG")]
    # Flatten list of lists and return image paths to caller
    return [str(path) for glob in glob_imgs for path in glob]
