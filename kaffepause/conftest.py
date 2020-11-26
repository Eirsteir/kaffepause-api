import pytest
from django.contrib.auth import get_user_model

from kaffepause.accounts.test.factories import AccountFactory
from kaffepause.breaks.models import Break, BreakInvitation
from kaffepause.breaks.test.factories import BreakFactory, BreakInvitationFactory
from kaffepause.friendships.enums import DefaultFriendshipStatus
from kaffepause.friendships.models import Friendship, FriendshipStatus
from kaffepause.friendships.test.factories import (
    FriendshipFactory,
    FriendshipStatusFactory,
)

Account = get_user_model()


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user() -> Account:
    return AccountFactory()


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


@pytest.fixture(autouse=True)
def study_break() -> Break:
    return BreakFactory(participants=(AccountFactory(),))


@pytest.fixture(autouse=True)
def break_invitation(study_break) -> BreakInvitation:
    return BreakInvitationFactory(subject=study_break, reply=None)
