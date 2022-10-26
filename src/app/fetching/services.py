import requests
import shutil
import json

from django.core.exceptions import RequestAborted
from django.conf import settings

from photos.services import PHOTOS_DIR
from photos.models import Photo


API_URL = "https://jsonplaceholder.typicode.com/photos"
DEFAULT_JSON_PATH = f"{settings.BASE_DIR.parent.parent}/photos.json"


def fetch_photos(start: int = 0, limit: int = None):
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
    with open(path, "r") as f:
        data = json.load(f)
    return data[start:] if not limit else data[start:start+limit]


def download_photo(filename: str, URL: str):
    URL = URL + ".png"
    r = requests.get(URL, stream=True)
    if r.status_code != 200:
        raise RequestAborted()
    with open(f"{PHOTOS_DIR}{filename}", 'wb') as f:
        r.raw.decode_content = True
        shutil.copyfileobj(r.raw, f)


def get_photo_name_from_url(URL: str) -> str:
    return URL.partition(".com")[2] + ".png"


def import_photos(photos: list[dict]) -> list[dict]:
    for photo in photos:
        name = get_photo_name_from_url(photo["url"])
        download_photo(name, photo["url"])
        data = {
            "title": photo["title"],
            "album_id": photo["albumId"],
            "URL": name,
        }
        Photo.objects.create(**data)
    return photos


def import_photos_from_api(
    start: int = 0, limit: int = None
) -> list[dict]:
    photos = fetch_photos(start, limit)
    return import_photos(photos)


def import_photos_from_json(
    path: str = DEFAULT_JSON_PATH,
    start: int = 0,
    limit: int = None
) -> list[dict]:
    photos = read_photos_from_json(path, start, limit)
    return import_photos(photos)
