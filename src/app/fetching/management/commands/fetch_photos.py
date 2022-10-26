from fetching.services import fetch_photos_to_database

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Fetches photos from remote API"

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            '--n', type=int, help="Number of photos to fetch"
        )

    def handle(self, *args, **options):
        n = None
        if options["n"]:
            n = options["n"]
        self.stdout.write('Fetching...')
        photos = fetch_photos_to_database(n)
        self.stdout.write(str(photos))
        self.stdout.write(self.style.SUCCESS('Done'))
