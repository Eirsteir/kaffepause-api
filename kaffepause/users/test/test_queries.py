from types import SimpleNamespace

import pytest

from kaffepause.users.test.factories import UserFactory
from kaffepause.users.test.graphql_requests import SEARCH_QUERY

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    "names, search_term, expected_matches",
    [
        (["Anders", "Andreas", "Henrik", "Anine"], "an", 3),
        (["Anders Nord", "Andreas Nord", "Henrik Nord", "Anine Nord"], " ", 4),
        (["Anders Nord", "Andreas Nord", "Henrik Nord", "Anine Nord"], " Nord", 4),
        (["Anders", "Andreas", "Henrik", "Anine"], "he", 1),
        (["Anders", "Andreas", "Henrik", "Anine"], "He", 1),
        (["Anders", "Andreas", "Henrik", "Anine"], " ", 0),
    ],
)
def test_search_by_name(
    client_query, auth_headers, names, search_term, expected_matches
):
    """Should return the users who's name matches the search query term."""
    for name in names:
        UserFactory(name=name, username="")

    variables = {"query": search_term}
    response = client_query(SEARCH_QUERY, variables=variables, headers=auth_headers)
    content = response.json(object_hook=lambda d: SimpleNamespace(**d))

    assert content.data.searchUsers.count == expected_matches


@pytest.mark.parametrize(
    "names, search_term, expected_matches",
    [
        (["Anders", "Andreas", "Henrik", "Anine"], "an", 3),
        (["Anders Nord", "Andreas Nord", "Henrik Nord", "Anine Nord"], " ", 4),
        (["Anders Nord", "Andreas Nord", "Henrik Nord", "Anine Nord"], " Nord", 4),
        (["Anders", "Andreas", "Henrik", "Anine"], "he", 1),
        (["Anders", "Andreas", "Henrik", "Anine"], "He", 1),
        (["Anders", "Andreas", "Henrik", "Anine"], " ", 0),
        (["Anders123", "Andreas", "Henrik123", "Anine"], "123", 2),
        (["Anders_", "Andreas", "Henrik_", "Anine"], "_", 2),
        (["Anders_", "Andreas", "Henrik_", "Anine"], "MATCH (n) RETURN n", 0),
    ],
)
def test_search_by_username(
    client_query, auth_headers, names, search_term, expected_matches
):
    """Should return the users who's username matches the search query term."""
    for name in names:
        UserFactory(name="", username=name)

    variables = {"query": search_term}
    response = client_query(SEARCH_QUERY, variables=variables, headers=auth_headers)
    content = response.json(object_hook=lambda d: SimpleNamespace(**d))

    assert content.data.searchUsers.count == expected_matches
