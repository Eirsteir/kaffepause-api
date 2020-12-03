import pytest
from neomodel import clear_neo4j_database, db

from kaffepause.users.models import User
from kaffepause.users.test.factories import UserFactory


@pytest.fixture(autouse=True)
def setup_and_teardown():
    clear_neo4j_database(db)
    yield
    clear_neo4j_database(db)


@pytest.fixture
def user() -> User:
    return UserFactory()
