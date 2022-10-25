from PIL import Image
from pathlib import Path

from django.conf import settings


def format_url(URL: str) -> str:
    base_dir = Path(settings.BASE_DIR).parent.parent
    return f"{base_dir}/photos{URL}"


def get_size(URL: str) -> tuple[int, int]:
    with Image.open(format_url(URL)) as img:
        width, height = img.size
    return (width, height)


def get_dominant_color(URL: str) -> str:
    # https://stackoverflow.com/a/61730849/19701843

    # Resize image to speed up processing
    img = Image.open(format_url(URL))
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
