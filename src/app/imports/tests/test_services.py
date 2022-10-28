from django.test import TestCase
from django.core.exceptions import RequestAborted

import shutil
import os

from unittest.mock import MagicMock, patch

from imports.services import (
    download_photo,
    fetch_photos,
    get_photo_name_from_url,
    import_photos,
    import_photos_from_api,
    import_photos_from_json,
    read_photos_from_json
)
from photos.services import PHOTOS_DIR
from photos.models import Photo


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


class TestImportsServices(TestCase):
    def setUp(self):
        remove_photos_dir()

    def test_download_photo(self):
        self.assertFalse(os.path.exists(PHOTOS_DIR))
        filename = "test_photo.png"
        download_photo(filename, "https://via.placeholder.com/600/92c952")
        self.assertTrue(os.path.exists(PHOTOS_DIR))
        self.assertTrue(os.path.exists(os.path.join(PHOTOS_DIR, filename)))

    def test_get_photo_name_from_url(self):
        url = "https://via.placeholder.com/600/92c952"
        filename = get_photo_name_from_url(url)
        self.assertEqual(filename, "92c952.png")

    @patch('imports.services.requests')
    def test_fetch_photos_200(self, mock):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock.get.return_value = mock_response
        fetch_photos()

    @patch('imports.services.requests')
    def test_fetch_photos_not_200(self, mock):
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock.get.return_value = mock_response
        with self.assertRaises(RequestAborted):
            fetch_photos()

    @patch('imports.services.requests')
    def test_fetch_photos_no_arguments(self, mock):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = EXAMPLE_PHOTOS
        mock.get.return_value = mock_response
        self.assertEqual(fetch_photos(), EXAMPLE_PHOTOS)

    def test_fetch_photos_with_limit(self):
        self.assertEqual(len(fetch_photos(limit=3)), 3)

    def test_fetch_photos_with_limit_and_start(self):
        photos = fetch_photos(start=3, limit=3)
        self.assertEqual(photos[0]["id"], 4)
        self.assertEqual(photos[2]["id"], 6)
        self.assertEqual(len(photos), 3)

    def test_import_photos(self):
        for file in ("92c952.png", "771796.png", "24f355.png", "d32776.png"):
            self.assertFalse(os.path.exists(os.path.join(PHOTOS_DIR, file)))
        import_photos(EXAMPLE_PHOTOS)
        for file in ("92c952.png", "771796.png", "24f355.png", "d32776.png"):
            self.assertTrue(os.path.exists(os.path.join(PHOTOS_DIR, file)))
        self.assertEqual(Photo.objects.count(), 4)

    @patch('imports.services.fetch_photos')
    def test_import_photos_from_api(self, mock):
        mock.return_value = EXAMPLE_PHOTOS

        for file in ("92c952.png", "771796.png", "24f355.png", "d32776.png"):
            self.assertFalse(os.path.exists(os.path.join(PHOTOS_DIR, file)))

        import_photos_from_api()

        for file in ("92c952.png", "771796.png", "24f355.png", "d32776.png"):
            self.assertTrue(os.path.exists(os.path.join(PHOTOS_DIR, file)))

        self.assertEqual(Photo.objects.count(), 4)

    @patch("imports.services.json.load")
    @patch("imports.services.open")
    def test_read_photos_from_json(self, _, mock_json_load):
        mock_json_load.return_value = EXAMPLE_PHOTOS
        self.assertEqual(read_photos_from_json("filepath"), EXAMPLE_PHOTOS)

    @patch("imports.services.json.load")
    @patch("imports.services.open")
    def test_read_photos_from_json_with_limit(self, _, mock_json_load):
        mock_json_load.return_value = EXAMPLE_PHOTOS
        self.assertEqual(
            read_photos_from_json("filepath", limit=3), EXAMPLE_PHOTOS[:3]
        )

    @patch("imports.services.json.load")
    @patch("imports.services.open")
    def test_read_photos_from_json_with_limit_start(self, _, mock_json_load):
        mock_json_load.return_value = EXAMPLE_PHOTOS
        self.assertEqual(
            read_photos_from_json(
                "filepath",
                start=1,
                limit=3
            ),
            EXAMPLE_PHOTOS[1:4]
        )

    @patch('imports.services.read_photos_from_json')
    def test_import_photos_from_json(self, mock):
        mock.return_value = EXAMPLE_PHOTOS

        for file in ("92c952.png", "771796.png", "24f355.png", "d32776.png"):
            self.assertFalse(os.path.exists(os.path.join(PHOTOS_DIR, file)))

        import_photos_from_json()

        for file in ("92c952.png", "771796.png", "24f355.png", "d32776.png"):
            self.assertTrue(os.path.exists(os.path.join(PHOTOS_DIR, file)))

        self.assertEqual(Photo.objects.count(), 4)
