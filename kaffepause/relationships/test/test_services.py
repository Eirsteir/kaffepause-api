import pytest
from neomodel import clear_neo4j_database, db

from kaffepause.relationships.services import send_friend_request
from kaffepause.users.test.factories import UserFactory

pytestmark = pytest.mark.django_db

# https://github.com/hspandher/django-test-addons#testing-neo4j-graph-database


@pytest.fixture(autouse=True)
def setup():
    clear_neo4j_database(db)


def test_send_friend_request():
    actor = UserFactory()
    to_user = UserFactory()

    result = send_friend_request(actor, to_user)
    print(result)

    assert False
