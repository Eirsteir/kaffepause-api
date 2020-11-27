import pytest

from kaffepause.relationships.services import send_friend_request
from kaffepause.users.test.factories import UserFactory

pytestmark = pytest.mark.django_db


@pytest.fixture(autouse=True)
def test_send_friend_request():
    actor = UserFactory().save()
    to_user = UserFactory().save()

    result = send_friend_request(actor, to_user)
    print(result)

    assert False
