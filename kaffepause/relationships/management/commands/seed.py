from django.core.management.base import BaseCommand

from kaffepause.users.test.factories import UserFactory


class Command(BaseCommand):
    help = "Seeds the database with relationships."

    def add_arguments(self, parser):
        parser.add_argument(
            "--relationships",
            default=100,
            type=int,
            help="The number of fake relationships to create.",
        )

    def handle(self, *args, **options):
        print("CREATING RELATIONSHIPS")
        for _ in range(options["relationship"] / 2):
            user = UserFactory().save()
            other = UserFactory().save()
            user.friends.connect(other)

        for _ in range(options["relationship"] / 2):
            user = UserFactory().save()
            other = UserFactory().save()
            user.outgoing_friend_requests.connect(other)
            other.incoming_friend_requests.connect(user)
