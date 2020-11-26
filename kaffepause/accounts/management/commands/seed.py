from django.core.management.base import BaseCommand

from kaffepause.accounts.test.factories import AccountFactory, UserStatusFactory


class Command(BaseCommand):
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
            user = AccountFactory()
            UserStatusFactory(user=user)
