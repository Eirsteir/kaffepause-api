from django.core.management.base import BaseCommand
from django.db import IntegrityError

from kaffepause.friendships.enums import FriendshipStatusEnum
from kaffepause.friendships.test.factories import (
    FriendshipFactory,
    FriendshipStatusFactory,
)


class Command(BaseCommand):
    help = "Seeds the database with friendship."

    def add_arguments(self, parser):
        parser.add_argument(
            "--friendship",
            default=400,
            type=int,
            help="The number of fake friendship to create.",
        )

    def handle(self, *args, **options):
        for status in FriendshipStatusEnum:
            try:
                FriendshipStatusFactory(name=status)
            except IntegrityError:
                print("Friendship status already exists: ", status)

        for _ in range(options["friendship"]):
            FriendshipFactory()
