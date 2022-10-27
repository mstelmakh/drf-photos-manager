from imports.services import import_photos_from_json

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Django CLI command used to import photos from local JSON file.

    Args:
        f: Path to json file (optional).
        start: Offset of first photo to import (optional).
        limit: Number of photos to import (optional).
    """
    help = "Imports photos from local JSON file."

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            '--f', type=str, help="Path to json file."
        )
        parser.add_argument(
            '--start', type=int,
            default=0,
            help="Offset of first photo to import (default: 0)."
        )
        parser.add_argument(
            '--limit', type=int, help="Number of photos to import."
        )

    def handle(self, *args, **options):
        path, limit = None, None
        if options["limit"]:
            limit = options["limit"]
        if options["f"]:
            path = options["f"]

        self.stdout.write('Importing...')

        if path:
            import_photos_from_json(path, options["start"], limit)
        else:
            import_photos_from_json(start=options["start"], limit=limit)

        self.stdout.write(self.style.SUCCESS('Done'))
