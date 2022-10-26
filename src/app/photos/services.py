from PIL import Image
from pathlib import Path

from django.conf import settings
from django.core.exceptions import ValidationError


PHOTOS_DIR = f"{Path(settings.BASE_DIR).parent.parent}/photos"


def get_size(URL: str) -> tuple[int, int]:
    """
    Finds image size.

    Args:
        URL: A path to an image.

    Returns:
        A tuple of two integer values.

    Raises:
        ValidationError: When there's no image with given path.
    """
    try:
        with Image.open(f"{PHOTOS_DIR}{URL}") as img:
            width, height = img.size
    except FileNotFoundError:
        raise ValidationError({"URL": "Invalid path."})
    return (width, height)


def get_dominant_color(URL: str) -> str:
    """
    Finds image dominant color.
    https://stackoverflow.com/a/61730849/19701843

    Args:
        URL: A path to an image.

    Returns:
        A string representing a color in hexadecimal system.

    Raises:
        ValidationError: When there's no image with given path.
    """
    try:
        img = Image.open(f"{PHOTOS_DIR}{URL}")
    except FileNotFoundError:
        raise ValidationError({"URL": "Invalid path."})
    img = img.copy()
    img.thumbnail((100, 100))

    # Reduce colors (uses k-means internally)
    paletted = img.convert('P', palette=Image.ADAPTIVE, colors=16)

    # Find the color that occurs most often
    palette = paletted.getpalette()
    color_counts = sorted(paletted.getcolors(), reverse=True)
    palette_index = color_counts[0][1]
    dominant_color = palette[palette_index*3:palette_index*3+3]

    return '#' + ''.join(f'{i:02X}' for i in dominant_color)


def save_analyzed_photo(f):
    """Decorator used to update photo's fields before saving."""
    def wrapper(photo, **kwargs):
        photo_size = get_size(photo.URL)
        photo.width, photo.height = photo_size
        photo.color = get_dominant_color(photo.URL)
        return f(photo, **kwargs)
    return wrapper
