import pytest

from kaffepause.friendships.enums import DefaultFriendshipStatus
from kaffepause.friendships.models import Friendship, FriendshipStatus
from kaffepause.friendships.test.factories import (
    FriendshipFactory,
    FriendshipStatusFactory,
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
def friendship() -> Friendship:
    return FriendshipFactory()


@pytest.fixture(autouse=True)
def are_friends_status() -> FriendshipStatus:
    return FriendshipStatusFactory.from_enum(DefaultFriendshipStatus.ARE_FRIENDS)


@pytest.fixture(autouse=True)
def requested_status() -> FriendshipStatus:
    return FriendshipStatusFactory.from_enum(DefaultFriendshipStatus.REQUESTED)


@pytest.fixture(autouse=True)
def blocked_status() -> FriendshipStatus:
    return FriendshipStatusFactory.from_enum(DefaultFriendshipStatus.BLOCKED)
