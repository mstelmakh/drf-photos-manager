from fetching.services import import_photos_from_json

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Imports photos from local JSON file."

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            '--f', type=str, help="Path to json file."
        )
        parser.add_argument(
            '--n', type=int, help="Number of photos to import."
        )

    def handle(self, *args, **options):
        path, n = None, None
        if options["n"]:
            n = options["n"]
        if options["f"]:
            path = options["f"]

        self.stdout.write('Importing...')

        import_photos_from_json(path, n)

        self.stdout.write(self.style.SUCCESS('Done'))
