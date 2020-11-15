from django.core.management.base import BaseCommand
from django.db import IntegrityError

from kaffepause.breaks.test.factories import BreakFactory, BreakInvitationFactory
from kaffepause.friendships.enums import DefaultFriendshipStatus
from kaffepause.friendships.test.factories import (
    FriendshipFactory,
    FriendshipStatusFactory,
)


class Command(BaseCommand):
    help = "Seeds the database with breaks and invitations."

    def add_arguments(self, parser):
        parser.add_argument(
            "--breaks",
            default=200,
            type=int,
            help="The number of fake objects to create.",
        )

    def handle(self, *args, **options):
        for _ in range(options["friendship"]):
            new_break = BreakFactory()
            BreakInvitationFactory(subject=new_break)
