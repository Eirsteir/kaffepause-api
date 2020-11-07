from django.core.management.base import BaseCommand

from kaffepause.users.test.factories import UserFactory


class Command(BaseCommand):
    help = "Seeds the database with users."

    def add_arguments(self, parser):
        parser.add_argument(
            "--users",
            default=100,
            type=int,
            help="The number of fake users to create.",
        )

    def handle(self, *args, **options):
        for _ in range(options["users"]):
            UserFactory.create()
