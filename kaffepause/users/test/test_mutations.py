from types import SimpleNamespace

import pytest

from kaffepause.users.test.factories import UserFactory
from kaffepause.users.test.graphql_requests import UPDATE_PROFILE_MUTATION

pytestmark = pytest.mark.django_db


@pytest.fixture
def proto_user():
    return UserFactory.build()


def get_update_data_for(user):
    return {
        "name": user.name,
        "username": user.username,
        "locale": user.locale,
    }


def test_update_profile_updates_user(client_query, auth_headers, user, proto_user):
    """Should return the updated user."""

    response = client_query(
        UPDATE_PROFILE_MUTATION,
        op_name="updateProfile",
        variables=get_update_data_for(proto_user),
        headers=auth_headers,
    )
    content = response.json(object_hook=lambda d: SimpleNamespace(**d))
    data = content.data.updateProfile
    actual_user = data.user

    assert actual_user.uuid == str(user.uuid)
    assert actual_user.name == proto_user.name
    assert actual_user.username == proto_user.username
    assert actual_user.locale == proto_user.locale


def test_update_profile_when_username_already_in_use(
    snapshot, client_query, auth_headers, user
):
    """Should not update the user when the username is in use."""
    taken_username = UserFactory().username
    user.username = taken_username

    response = client_query(
        UPDATE_PROFILE_MUTATION,
        op_name="updateProfile",
        variables=get_update_data_for(user),
        headers=auth_headers,
    )
    content = response.json()
    snapshot.assert_match(content)


def test_update_profile_when_unauthenticated(snapshot, client_query, user):
    """Should not update the user when the user is not authenticated."""
    response = client_query(
        UPDATE_PROFILE_MUTATION,
        op_name="updateProfile",
        variables=get_update_data_for(user),
    )
    content = response.json()

    snapshot.assert_match(content)
