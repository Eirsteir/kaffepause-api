from django.conf import settings
from django.core.management.base import BaseCommand
from neomodel import clear_neo4j_database, db

from kaffepause.accounts.test.factories import AccountFactory, UserStatusFactory
from kaffepause.breaks.enums import BreakRelationship
from kaffepause.relationships.enums import UserRelationship
from kaffepause.users.test.factories import UserFactory

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

        if not settings.DEBUG:
            raise Exception("Can only seed database in development")

        for _ in range(options["accounts"]):
            account = AccountFactory()
            UserStatusFactory(user=account)
            UserFactory(uuid=account.id)

        # Command.populate_with_random_data()
        Command.create_random_friendships()
        Command.create_random_friend_requests()
        Command.create_random_break_and_invites()
        Command.create_random_break_and_invites_connections()

    @staticmethod
    def populate_with_random_data(range_min=1, range_max=200):
        """ Populate database with a defined number of random users """
        query = """
        WITH $names AS names_list
        FOREACH (r IN range($range_min, $range_max) |
            CREATE (:User {id:r,
                    uuid: apoc.create.uuid(),
                    username:names_list[toInteger(size(names_list)*rand())] + r
                    }));
        """
        params = dict(names=NAMES, range_min=range_min, range_max=range_max)
        return db.cypher_query(query, params)

    @staticmethod
    def create_random_friendships():
        """
        Populate actual database with random friendships between users
        """
        query = f"""
        MATCH (u:User), (s:User)
        WITH u, s
        LIMIT 10000
        WHERE rand() < 0.2 AND u <> s
        AND NOT (u)-[:{UserRelationship.REQUESTING_FRIENDSHIP}]-(s)
        MERGE (u)-[:{UserRelationship.ARE_FRIENDS}]-(s)
        MERGE (u)-[:{UserRelationship.FOLLOWING}]->(s)
        MERGE (s)-[:{UserRelationship.FOLLOWING}]->(u)
        """
        return db.cypher_query(query)

    @staticmethod
    def create_random_friend_requests():
        """
        Populate actual database with random friend requests between users
        """
        query = f"""
        MATCH (u:User), (s:User)
        WITH u, s
        LIMIT 10000
        WHERE rand() < 0.2 AND u <> s
        AND NOT (u)-[:{UserRelationship.ARE_FRIENDS}]-(s)
        MERGE (u)-[:{UserRelationship.REQUESTING_FRIENDSHIP}]-(s)
        """
        return db.cypher_query(query)

    @staticmethod
    def create_random_break_and_invites(range_min=1, range_max=50):
        """
        Populate actual database with random breaks and invitations
        """
        query = """
        FOREACH (r IN range($range_min, $range_max) |
        CREATE (b:Break {uuid: apoc.create.uuid(),
            starting_at: datetime().epochSeconds + (1000*60*r)
        })
        CREATE (i:BreakInvitation {uuid: apoc.create.uuid()})
        CREATE (i)-[:REGARDING]->(b));
        """

        params = dict(range_min=range_min, range_max=range_max)
        return db.cypher_query(query, params=params)

    @staticmethod
    def create_random_break_and_invites_connections():
        """
        Populate actual database with random connections between breaks, invitations and users
        """
        query = f"""
        MATCH (u:User), (s:User), (b:Break), (i:BreakInvitation)
        WITH u, s, b, i
        LIMIT 10000
        WHERE rand() < 0.2 AND u <> s
        AND (u)-[:{UserRelationship.ARE_FRIENDS}]-(s)
        AND NOT ()-[:{BreakRelationship.SENT}]->(i)
        MERGE (u)-[:{BreakRelationship.SENT}]->(i)
        MERGE (i)-[:{BreakRelationship.TO}]->(s)
        MERGE (u)-[:{BreakRelationship.PARTICIPATED_IN}]->(b)
        """

        return db.cypher_query(query)


# UNWIND range(1,100) as id
# CREATE (p:Person {id:id, name: "Name " + id, age: id % 3}) WITH collect(p) as people
# UNWIND people as p1
# UNWIND range(1,10) as friend
# WITH p1, people[(p1.id + friend) % size(people)] as p2
# CREATE (p1)-[:KNOWS {years: abs(p2.id - p1.id)}]->(p2)
