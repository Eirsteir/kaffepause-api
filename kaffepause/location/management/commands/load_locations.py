import json
import urllib.request
from os.path import exists

from django.core.management.base import BaseCommand


from kaffepause.location.models import Location

JSON_DATA_FILE = 'kaffepause/locations.json'
LOCATIONS_API = "https://api.mazemap.com/api/webappconfig/default/"


class Command(BaseCommand):

    help = "Seeds the database with location data from a third party API."

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            default=False,
            type=bool,
            help=f"Force locations to be reloaded from {JSON_DATA_FILE}",
        )
        parser.add_argument(
            "--force_download",
            default=False,
            type=bool,
            help=f"Force a download from {LOCATIONS_API}",
        )

    def handle(self, *args, **options):
        if len(Location.nodes.all()) and not options["force"]:
            print("Locations already loaded. Use --force to reload.")
            return

        output = self.download_if_necessary(options["force_download"])
        locations = output["campusMenu"]["children"]
        self._parse_locations(locations)

    def download_if_necessary(self, force_download):
        if force_download or not exists(JSON_DATA_FILE):
            print("Downloading data...")
            data = urllib.request.urlopen(LOCATIONS_API).read()
            output = json.loads(data)

            print(f"Writing data to {JSON_DATA_FILE}...")
            with open(JSON_DATA_FILE, 'w') as outfile:
                json.dump(output, outfile, indent=4)

        print(f"Loading data from {JSON_DATA_FILE}...")
        with open(JSON_DATA_FILE) as json_file:
            output = json.load(json_file)

        return output


    def _parse_locations(self, json):
        for item in json:
            parent = self._parse_location(item)
            parent.save()
            self._walk_tree(item["children"], parent)

    def _walk_tree(self, json, parent):
        for item in json:
            child = self._parse_location(item)
            child.save()
            parent.children.connect(child)
            self._walk_tree(item["children"], child)

    def _parse_location(self, json):
        type_ = json["type"] if json["type"] else None
        item_type = json["itemType"] if json["itemType"] else None

        return Location(title=json["title"], type=type_, item_type=item_type)
