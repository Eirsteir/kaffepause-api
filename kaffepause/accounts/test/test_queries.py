import pytest

from kaffepause.accounts.test.graphql_requests import MY_ACCOUNT_QUERY

pytestmark = pytest.mark.django_db


def test_account_query_returns_the_users_account(client_query, auth_headers, account):
    """Should return the current users account."""
    response = client_query(MY_ACCOUNT_QUERY, headers=auth_headers)
    content = response.json()

    actual_account_uuid = content.get("data").get("myAccount").get("uuid")

    assert actual_account_uuid == str(account.id)


def test_account_query_unauthenticated(snapshot, client_query):
    """Should not be permitted to get own account when unauthenticated."""
    response = client_query(MY_ACCOUNT_QUERY)
    content = response.json()

    snapshot.assert_match(content)
