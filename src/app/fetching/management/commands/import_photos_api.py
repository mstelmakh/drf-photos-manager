from fetching.services import import_photos_from_api

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Imports photos from remote API."

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            '--n', type=int, help="Number of photos to import."
        )

    def handle(self, *args, **options):
        n = None
        if options["n"]:
            n = options["n"]

        self.stdout.write('Importing...')

        import_photos_from_api(n)

        self.stdout.write(self.style.SUCCESS('Done'))
