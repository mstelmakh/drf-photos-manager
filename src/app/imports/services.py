import requests
import shutil
import json
import os

from django.core.exceptions import RequestAborted
from django.conf import settings

from photos.services import PHOTOS_DIR
from photos.models import Photo


API_URL = "https://jsonplaceholder.typicode.com/photos"
DEFAULT_JSON_PATH = os.path.join(
    settings.BASE_DIR.parent, "photos.json"
)


def fetch_photos(start: int = 0, limit: int = None):
    """
    Fetches photos from external API.

    Args:
        start: Offset of first fetched photo.
        limit: Limit of number of photos.

    Returns:
        JSON encoded list of photos.

    Raises:
        RequestAborted: If there's an error occured while fetching photos.
    """
    url = f"{API_URL}?_start={start}"
    if limit:
        url += f"&_limit={limit}"

    r = requests.get(url, headers={
        'Content-Type':
        'application/json'
    })

    if r.status_code != 200:
        raise RequestAborted()
    photos = r.json()
    return photos


def read_photos_from_json(
    path: str,
    start: int = 0,
    limit: int = None
) -> list[dict]:
    """
    Reads photos from JSON file.

    Args:
        path: Path to JSON file.
        start: Offset of first photo.
        limit: Limit of number of photos.

    Returns:
        JSON encoded list of photos.
    """
    with open(path, "r") as f:
        data = json.load(f)
    return data if not limit else data[start:start+limit]


def download_photo(filename: str, URL: str):
    """
    Downloads photo from given URL.

    Args:
        filename: Name of the saved photo (relative to /photos directory).
        URL: URL to photo.

    Raises:
        RequestAborted: If there's an error occured while downloading photo.
    """
    URL = URL + ".png"
    r = requests.get(URL, stream=True)
    print(f"DIR: {PHOTOS_DIR}{filename}")
    if not os.path.exists(PHOTOS_DIR):
        os.makedirs(PHOTOS_DIR)
    if r.status_code != 200:
        raise RequestAborted()
    with open(f"{PHOTOS_DIR}{filename}", 'wb') as f:
        r.raw.decode_content = True
        shutil.copyfileobj(r.raw, f)


def get_photo_name_from_url(URL: str) -> str:
    """
    Formats photo name according to its URL.

    Args:
        URL: URL to photo.

    Returns:
        String containing everything that is after last '/' in URL + '.png'.
    """
    return f"/{URL.rpartition('/')[-1]}.png"


def import_photos(photos: list[dict]):
    """
    Saves given photos to database.

    Args:
        photos: JSON encoded list of photos to save.
    """
    for photo in photos:
        name = get_photo_name_from_url(photo["url"])
        print(name)
        # Probably it would be better to use async
        download_photo(name, photo["url"])
        data = {
            "title": photo["title"],
            "album_id": photo["albumId"],
            "URL": name,
        }
        Photo.objects.create(**data)


def import_photos_from_api(
    start: int = 0, limit: int = None
) -> list[dict]:
    """
    Imports photos from external API to database.

    Args:
        URL: URL to photo.
        start: Offset of first fetched photo.
        limit: Limit of number of photos.

    Returns:
        JSON encoded list of saved photos.
    """
    photos = fetch_photos(start, limit)
    import_photos(photos)
    return photos


def import_photos_from_json(
    path: str = DEFAULT_JSON_PATH,
    start: int = 0,
    limit: int = None
) -> list[dict]:
    """
    Imports photos from JSON file to database.

    Args:
        path: Path to JSON file.
        start: Offset of first photo.
        limit: Limit of number of photos.

    Returns:
        JSON encoded list of saved photos.
    """
    photos = read_photos_from_json(path, start, limit)
    import_photos(photos)
    return photos
