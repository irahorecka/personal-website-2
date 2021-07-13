"""
"""

from pathlib import Path

GALLERY_PATH = Path(__file__).absolute().parent.parent.parent / "static" / "images" / "gallery"
CONTENT = {
    "home": {
        "header": {
            "first": "Ira Horecka",
            "second": "What the heck do I do?",
            "third": "Do I step away from my computer?",
        },
        "body": {
            "first": "Hello, I'm Ira. I enjoy programming and will join the University of Toronto this fall to study computational biology as a PhD candidate.",
            "second": "I live in Mountain View, CA and work as a lab automation engineer. I have an educational background in biochemistry & molecular biology. I started programming almost 3 years ago and have enjoyed it since.",
            "third": 'There was a period in time when I worked as a research associate (RA) at pharmaceutical firms. I always wondered, "How do I break out of the RA title? Did I study a rigorous curriculum to become adept at pipetting?" Before I delve further, I do not intend to undermine RAs, as the career is fulfilling in its own light.',
            "fourth": "My twin brother is a software engineer and he encouraged me to take up programming, so I did. I eventually moved on to become a lab automation engineer, programming liquid handlers to automate laboratory procedures. I strive to go beyond programming robots, which is why I'm pursuing a higher education in computational biology - to merge my academic background with my passion in software development.",
            "fifth": "Yes! I enjoy refurbishing bicycles and bass fishing when I'm away from my computer. These hobbies are frustrating and fulfilling, which is a common emotional elixir in any activity with a learning curve; and when things go according to plan, the world is briefly wonderful.",
        },
    },
    "api": {
        "header": {"first": "It's API time"},
        "body": {
            "first": "I enjoy writing API wrappers in Python. Take a look at my REST API for Craigslist housing in the SF Bay Area."
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
    glob_imgs = [
        list(map(lambda x: str(x), GALLERY_PATH.glob(ext)))
        for ext in ("*.png", "*.PNG", "*.jpeg", "*.JPEG", "*.jpg", "*.JPG")
    ]
    # Flatten list of lists and return paths to caller
    return [path for glob in glob_imgs for path in glob]
