import json
import urllib.request

from django.core.management.base import BaseCommand

from kaffepause.location.models import Location

LOCATIONS_API = "https://api.mazemap.com/api/webappconfig/default/"


class Command(BaseCommand):

    help = "Seeds the database with location data from a third party API."

    def handle(self, *args, **options):
        data = urllib.request.urlopen(LOCATIONS_API).read()
        output = json.loads(data)

        locations = output["campusMenu"]["children"]
        self._parse_locations(locations)

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
