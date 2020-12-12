import pytest

from kaffepause.users.models import User
from kaffepause.users.test.graphql_requests import UPDATE_PROFILE_MUTATION

pytestmark = pytest.mark.django_db


def test_update_profile_updates_profile(client_query, auth_headers, user):
    """Should update the given fields on the user."""
    expected_name = "New name"
    expected_username = "New username"

    variables = {"name": expected_name, "username": expected_username}

    client_query(
        UPDATE_PROFILE_MUTATION,
        op_name="updateProfile",
        variables=variables,
        headers=auth_headers,
    )
    user.refresh()

    assert user.name == expected_name
    assert user.username == expected_username


def test_update_profile_when_username_already_in_use(client_query, auth_headers, user):
    """Should not update the user when the username is in use."""
    expected_name = "New name"
    expected_username = user.username
    User(name="test", username=expected_username).save()

    variables = {"name": expected_name, "username": expected_username}

    response = client_query(
        UPDATE_PROFILE_MUTATION,
        op_name="updateProfile",
        variables=variables,
        headers=auth_headers,
    )
    content = response.json()
    data = content.get("data").get("updateProfile")

    assert "errors" in data


def test_update_profile_when_username_already_in_use_by_updater(
    client_query, auth_headers, user
):
    """Should still update other fields if username is in use by the one performing the update."""
    expected_name = "New name"
    expected_username = user.username

    variables = {"name": expected_name, "username": expected_username}

    client_query(
        UPDATE_PROFILE_MUTATION,
        op_name="updateProfile",
        variables=variables,
        headers=auth_headers,
    )
    user.refresh()

    assert user.name == expected_name
    assert user.username == expected_username


def test_update_profile_when_unauthenticated(snapshot, client_query):
    """Should not update the user when the user is not authenticated."""

    variables = {"name": "test", "username": "test"}

    response = client_query(
        UPDATE_PROFILE_MUTATION, op_name="updateProfile", variables=variables
    )
    content = response.json()

    snapshot.assert_match(content)
