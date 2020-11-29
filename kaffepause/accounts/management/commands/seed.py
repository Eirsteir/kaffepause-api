from django.core.management.base import BaseCommand
from neomodel import NeomodelException, db

from kaffepause.accounts.test.factories import AccountFactory, UserStatusFactory
from kaffepause.relationships.enums import ARE_FRIENDS

NAMES = ["anna", "andrew", "tom", "leroy", "stenli", "jeff", "jack", "karol"]


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

        try:
            Command.populate_with_random_data()
            Command.create_random_connections()
        except NeomodelException as e:
            print(e)

    @staticmethod
    def create_random_connections():
        """
        Populate actual database with random connections between users
        """
        query = f"""
        MATCH (u:User), (s:User)
        WITH u, s
        LIMIT 10000
        WHERE rand() < 0.2 AND u <> s
        MERGE (u)-[:{ARE_FRIENDS}]-(s);
        """
        return db.cypher_query(query)

    @staticmethod
    def populate_with_random_data(range_min=1, range_max=200):
        """ Populate database with a defined number of random users """
        query = """
        WITH {names} AS names_list
        FOREACH (r IN range({range_min},{range_max}) |
            CREATE (:User {id:r,
                    username:names_list[toInt(size(names_list)*rand())] + r
                    }));
        """
        params = dict(names=NAMES, range_min=range_min, range_max=range_max)
        return db.cypher_query(query, params)
