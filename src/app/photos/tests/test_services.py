from dataclasses import dataclass
from django.test import TestCase

import os
import shutil

from photos.services import (
    get_size,
    get_dominant_color,
    save_analyzed_photo,
    PHOTOS_DIR
)

from imports.services import download_photo, get_photo_name_from_url


EXAMPLE_PHOTOS = [
    {
        "albumId": 1,
        "id": 1,
        "title": "accusamus beatae ad facilis cum similique qui sunt",
        "url": "https://via.placeholder.com/600/92c952",
        "thumbnailUrl": "https://via.placeholder.com/150/92c952"
    },
    {
        "albumId": 1,
        "id": 2,
        "title": "reprehenderit est deserunt velit ipsam",
        "url": "https://via.placeholder.com/600/771796",
        "thumbnailUrl": "https://via.placeholder.com/150/771796"
    },
    {
        "albumId": 1,
        "id": 3,
        "title": "officia porro iure quia iusto qui ipsa ut modi",
        "url": "https://via.placeholder.com/600/24f355",
        "thumbnailUrl": "https://via.placeholder.com/150/24f355"
    },
    {
        "albumId": 1,
        "id": 4,
        "title": "culpa odio esse rerum omnis laboriosam voluptate repudiand",
        "url": "https://via.placeholder.com/600/d32776",
        "thumbnailUrl": "https://via.placeholder.com/150/d32776"
    }
]


def remove_photos_dir():
    if os.path.exists(PHOTOS_DIR):
        shutil.rmtree(PHOTOS_DIR)


def get_photo_size_from_url(url: str) -> int:
    """
    Gets photo size from its url.
    Assumes that number between last two slashes in url is photo's size.
    """
    return int(f"{url.split('/')[-2]}")


def get_photo_color_from_url(url: str) -> int:
    """
    Gets photo dominant color from its url.
    Assumes that hex number after last slash in url is photo's color.
    """
    return f"{url.split('/')[-1]}"


class TestPhotosServices(TestCase):
    def setUp(self):
        self.photos = []
        for photo in EXAMPLE_PHOTOS:
            size = get_photo_size_from_url(photo["url"])
            color = get_photo_color_from_url(photo["url"])
            name = get_photo_name_from_url(photo["url"])
            self.photos.append({"name": name, "color": color, "size": size})
            download_photo(name, photo["url"])

    def tearDown(self):
        remove_photos_dir()

    def test_get_size(self):
        for photo in self.photos:
            with self.subTest():
                size = get_size(photo["name"])
                self.assertEqual(size, (photo["size"], photo["size"]))

    def test_get_dominant_color(self):
        for photo in self.photos:
            with self.subTest():
                color = get_dominant_color(photo["name"])
                self.assertEqual(color.upper(), f"#{photo['color']}".upper())

    def test_save_analyzed_photo(self):
        @dataclass
        class Photo:
            id: int
            title: str
            album_id: int
            URL: str
            width: int = None
            height: int = None
            color: str = None

        photo_json = EXAMPLE_PHOTOS[0]

        photo = Photo(
            id=photo_json["id"],
            title=photo_json["title"],
            album_id=photo_json["albumId"],
            URL=get_photo_name_from_url(photo_json["url"])
        )

        self.assertIsNone(photo.width)
        self.assertIsNone(photo.height)
        self.assertIsNone(photo.color)

        save_analyzed_photo(lambda _: _)(photo)

        self.assertIsNotNone(photo.width)
        self.assertIsNotNone(photo.height)
        self.assertIsNotNone(photo.color)
