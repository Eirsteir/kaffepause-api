from uuid import uuid4

from django.core.management.base import BaseCommand
from neomodel import NeomodelException, db

from kaffepause.accounts.test.factories import AccountFactory, UserStatusFactory
from kaffepause.breaks.enums import BreakRelationship
from kaffepause.relationships.enums import UserRelationship
from kaffepause.users.test.factories import UserFactory

NAMES = ["anna", "andrew", "tom", "leroy", "stenli", "jeff", "jack", "karol"]
UUIDS = [uuid4() for _ in range(8)]


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
        for uuid in UUIDS:
            account = AccountFactory(id=uuid)
            UserStatusFactory(user=account)
            UserFactory(uid=uuid)

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
        MATCH (u:User), (s:User), (b:Break), (i:BreakInvitation)
        WITH u, s, b, i
        LIMIT 10000
        WHERE rand() < 0.2 AND u <> s
        MERGE (u)-[:{UserRelationship.ARE_FRIENDS}]-(s)
        MERGE (u)-[:{BreakRelationship.SENT}]->(i)
        MERGE (i)-[:{BreakRelationship.REGARDING}]->(b)
        MERGE (i)-[:{BreakRelationship.TO}]->(s)
        MERGE (u)-[:{BreakRelationship.PARTICIPATED_IN}]->(b)
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
                    })
            CREATE (b:Break {id: r*r, start_time: datetime().epochSeconds + (1000*60*r)})
            CREATE (i:BreakInvitation {id: r*r*r})
            CREATE (i)-[:REGARDING]->(b)
            );
        """
        params = dict(names=NAMES, range_min=range_min, range_max=range_max)
        return db.cypher_query(query, params)
