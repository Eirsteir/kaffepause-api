import json

import pytest
from graphene_django.utils.testing import graphql_query

from kaffepause.statusupdates.enums import StatusUpdateType

pytestmark = pytest.mark.django_db


@pytest.fixture
def client_query(client):
    def func(*args, **kwargs):
        return graphql_query(*args, **kwargs, client=client)

    return func


def test_some_query(client_query):
    response = client_query(
        """
        mutation updateStatus($statusType: StatusUpdateType!) {
            updateStatus(statusType: $statusType) {
                currentStatus {
                    verb
                    created
                }
            }
        }
        """,
        op_name="updateStatus",
        variables={"statusType": StatusUpdateType.FOCUSMODE.name},
    )
    content = json.loads(response.content)
    print(content)
    assert "errors" not in content
