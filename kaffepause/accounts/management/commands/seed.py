from django.core.management.base import BaseCommand
from neomodel import NeomodelException

from kaffepause.accounts.test.factories import AccountFactory, UserStatusFactory
from kaffepause.users.models import User
from kaffepause.users.test.factories import UserFactory


class Command(BaseCommand):
    """Creates accounts, users and relationships. Was not able to run these in relationship app."""

    help = "Seeds the database with user accounts."

    def add_arguments(self, parser):
        parser.add_argument(
            "--accounts",
            default=100,
            type=int,
            help="The number of fake accounts to create.",
        )

    def handle(self, *args, **options):
        for _ in range(options["accounts"]):
            account = AccountFactory()
            UserStatusFactory(user=account)
            user = UserFactory(uid=account.id)
            other = UserFactory()

            try:
                user = User.get_or_create(user)[0]
                other = User.get_or_create(other)[0]
                user.friends.connect(other)
            except NeomodelException as e:
                print(e)

        for _ in range(options["accounts"]):
            user = UserFactory()
            other = UserFactory()
            try:
                user = User.get_or_create(user)[0]
                other = User.get_or_create(other)[0]

                user.outgoing_friend_requests.connect(other)
                other.incoming_friend_requests.connect(user)
            except NeomodelException as e:
                print(e)
