from irahorecka.python.content.config import GALLERY_PATH


def get_gallery_imgs():
    """Returns JPEG and PNG filenames in irahorecka/static/images/gallery to caller."""
    # Note: all images in irahorecka/static/images/gallery must be jpeg or png filetypes
    glob_imgs = [
        list(map(lambda x: str(x), GALLERY_PATH.glob(ext)))
        for ext in ("*.png", "*.PNG", "*.jpeg", "*.JPEG", "*.jpg", "*.JPG")
    ]
    # Flatten list of lists and return paths to caller
    return [path for glob in glob_imgs for path in glob]
