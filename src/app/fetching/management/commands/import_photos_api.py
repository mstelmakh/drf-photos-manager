from fetching.services import import_photos_from_api

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Django CLI command used to import photos from external API.

    Args:
        start: Offset of first photo to import (optional).
        limit: Number of photos to import (optional).
    """
    help = "Imports photos from remote API."

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            '--start', type=int,
            default=0,
            help="Offset of first photo to import (default: 0)."
        )
        parser.add_argument(
            '--limit', type=int, help="Number of photos to import."
        )

    def handle(self, *args, **options):
        limit = None
        if options["limit"]:
            limit = options["limit"]

        self.stdout.write('Importing...')

        import_photos_from_api(options["start"], limit)

        self.stdout.write(self.style.SUCCESS('Done'))
