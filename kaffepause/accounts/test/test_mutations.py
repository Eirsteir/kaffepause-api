from unittest.mock import patch
from uuid import UUID

import pytest
from graphql_jwt.settings import jwt_settings
from neomodel import NeomodelException

from kaffepause.accounts.models import Account
from kaffepause.accounts.test.graphql_requests import (
    DELETE_ACCOUNT_MUTATION,
    REGISTER_MUTATION,
)
from kaffepause.users.models import User

pytestmark = pytest.mark.django_db


def get_registration_data():
    expected_email = "test@test.com"
    expected_name = "Test"
    variables = {
        "name": expected_name,
        "email": expected_email,
        "password1": "not_a_secret",
        "password2": "not_a_secret",
    }
    return expected_email, expected_name, variables


def test_register_creates_account_and_user_successfully_creates_both(client_query):
    """Should create an account and corresponding user."""
    expected_email, expected_name, variables = get_registration_data()

    client_query(REGISTER_MUTATION, op_name="register", variables=variables)

    actual_account = Account.objects.get(email=expected_email)
    actual_user = User.nodes.get(uid=actual_account.id)

    assert actual_account.id == UUID(actual_user.uid)
    assert actual_user.name == expected_name
    assert actual_account.email == expected_email


@patch("kaffepause.users.models.User.save")
def test_register_deletes_account_when_user_creation_failed(mock_save, client_query):
    """The new account should be deleted if the user could not be created."""
    mock_save.side_effect = NeomodelException
    expected_email, expected_name, variables = get_registration_data()

    client_query(REGISTER_MUTATION, op_name="register", variables=variables)

    assert not Account.objects.filter(email=expected_email).exists()
    assert not User.nodes.get_or_none(name=expected_name)


def test_register_creates_account_and_user_when_graphql_auth_fails(client_query):
    """Should not create an account or a user when graphql auth fails to create the account."""
    expected_email, expected_name, variables = get_registration_data()
    variables.__setitem__("password1", "password")  # Too common password

    client_query(REGISTER_MUTATION, op_name="register", variables=variables)

    assert not Account.objects.filter(email=expected_email).exists()
    assert not User.nodes.get_or_none(name=expected_name)


def test_delete_account_deletes_account_and_user(client_query, account, user, token):
    """Should delete both the account and the user."""
    password = "not_a_secret"
    account.set_password(password)
    account.save()

    variables = {"password": password}
    client_query(
        DELETE_ACCOUNT_MUTATION,
        op_name="deleteAccount",
        variables=variables,
        headers={jwt_settings.JWT_AUTH_HEADER_NAME: token},
    )

    assert not Account.objects.filter(id=account.id).exists()
    assert not User.nodes.get_or_none(uid=user.uid)


def test_delete_account(snapshot, client_query, account, user, token):
    password = "not_a_secret"
    account.set_password(password)
    account.save()

    variables = {"password": password}
    response = client_query(
        DELETE_ACCOUNT_MUTATION,
        op_name="deleteAccount",
        variables=variables,
        headers={jwt_settings.JWT_AUTH_HEADER_NAME: token},
    )
    content = response.json()

    snapshot.assert_match(content)
