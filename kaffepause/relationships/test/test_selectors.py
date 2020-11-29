import pytest

from kaffepause.relationships.selectors import get_mutual_friends_count
from kaffepause.users.test.factories import UserFactory

pytestmark = pytest.mark.django_db


def test_get_mutual_friends_count():
    """Should return the number of mutual friends between the given users."""
    actor = UserFactory()
    user = UserFactory()
    mutual_friend = UserFactory()

    actor.friends.connect(user)
    actor.friends.connect(mutual_friend)

    user.friends.connect(mutual_friend)

    # Make sure others are not included
    actor.friends.connect(UserFactory())
    user.friends.connect(UserFactory())

    mutual_friends_count = get_mutual_friends_count(actor, user)

    assert mutual_friends_count == 1
