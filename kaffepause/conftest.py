import pytest

from kaffepause.relationships.enums import RelationshipStatusEnum
from kaffepause.relationships.models import Relationship, RelationshipStatus
from kaffepause.relationships.test.factories import (
    RelationshipFactory,
    RelationshipStatusFactory,
)
from kaffepause.users.models import User
from kaffepause.users.test.factories import UserFactory


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user() -> User:
    return UserFactory()


@pytest.fixture
def relationship() -> Relationship:
    return RelationshipFactory()


@pytest.fixture(autouse=True)
def are_friends_status() -> RelationshipStatus:
    return RelationshipStatusFactory(slug=RelationshipStatusEnum.ARE_FRIENDS)


@pytest.fixture(autouse=True)
def requested_status() -> RelationshipStatus:
    return RelationshipStatusFactory(slug=RelationshipStatusEnum.REQUESTED)


@pytest.fixture(autouse=True)
def blocked_status() -> RelationshipStatus:
    return RelationshipStatusFactory(slug=RelationshipStatusEnum.BLOCKED)
