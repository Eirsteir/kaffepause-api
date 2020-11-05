import pytest

from kaffepause.friendships.models import Friendship
from kaffepause.friendships.test.factories import FriendshipFactory
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
