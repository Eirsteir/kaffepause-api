import json

import pytest
from graphene_django.utils.testing import graphql_query

from kaffepause.statusupdates.enums import StatusUpdateType
from kaffepause.statusupdates.test.graphql_requests import UPDATE_STATUS_MUTATION

pytestmark = pytest.mark.django_db


@pytest.fixture
def client_query(client):
    def func(*args, **kwargs):
        return graphql_query(*args, **kwargs, client=client)

    return func


def test_update_status(client_query):

    response = client_query(
        UPDATE_STATUS_MUTATION,
        op_name="updateStatus",
        variables={"statusType": StatusUpdateType.FOCUSMODE.name},
    )
    content = response.json()
    print(response.__dict__)
    pytest.fail()
    assert "errors" not in content
