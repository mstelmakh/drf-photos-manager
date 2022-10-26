import requests
import shutil
from django.core.exceptions import RequestAborted


from photos.services import PHOTOS_DIR
from photos.models import Photo


def fetch_photos(n=None):
    url = "https://jsonplaceholder.typicode.com/photos"
    r = requests.get(url, headers={
        'Content-Type':
        'application/json'
    })
    if r.status_code != 200:
        raise RequestAborted()
    photos = r.json()
    return photos if not n else photos[:n]


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


def fetch_photos_to_database(n=None):
    photos = fetch_photos(n)
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
