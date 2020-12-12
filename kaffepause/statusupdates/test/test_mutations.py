import json

import pytest
from graphene_django.utils.testing import graphql_query
from graphql_jwt.settings import jwt_settings
from graphql_jwt.shortcuts import get_token
from graphql_jwt.testcases import JSONWebTokenTestCase

from kaffepause.statusupdates.enums import StatusUpdateType
from kaffepause.statusupdates.test.graphql_requests import UPDATE_STATUS_MUTATION

pytestmark = pytest.mark.django_db


@pytest.fixture
def token(account):
    return f"{jwt_settings.JWT_AUTH_HEADER_PREFIX} {get_token(account)}"


@pytest.fixture
def client_query(client):
    def func(*args, **kwargs):
        return graphql_query(*args, **kwargs, client=client)

    return func


def test_update_status_updates_users_current_status(client_query, token, user):
    """Should update the users current status to one of the given status type."""
    expected_status_type = StatusUpdateType.FOCUSMODE.name

    client_query(
        UPDATE_STATUS_MUTATION,
        op_name="updateStatus",
        variables={"statusType": expected_status_type},
        headers={jwt_settings.JWT_AUTH_HEADER_NAME: token},
    )

    assert user.current_status.single().status_type == expected_status_type


def test_update_status_returns_current_status(client_query, token, user):
    """Should return the newly updated status."""
    expected_status_type = StatusUpdateType.FOCUSMODE.name
    response = client_query(
        UPDATE_STATUS_MUTATION,
        op_name="updateStatus",
        variables={"statusType": expected_status_type},
        headers={jwt_settings.JWT_AUTH_HEADER_NAME: token},
    )
    content = response.json()
    print(content)
    assert (
        content.get("data").get("updateStatus").get("currentStatus").get("statusType")
        == expected_status_type
    )
