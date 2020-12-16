from datetime import timedelta
from uuid import UUID

import pytest
from django.utils import timezone

from kaffepause.breaks.test.graphql_requests import INITIATE_BREAK_MUTATION

pytestmark = pytest.mark.django_db


def expected_initiate_break_response(break_, initiator):
    invitation = break_.get_invitation()
    break_uuid = str(UUID(break_.uuid))
    invitation_uuid = str(UUID(invitation.uuid))
    initiator_uuid = str(initiator.uuid)
    return {
        "data": {
            "initiateBreak": {
                "break_": {
                    "uuid": break_uuid,
                    "startingAt": break_.starting_at.isoformat(),
                    "invitation": {
                        "uuid": invitation_uuid,
                        "created": invitation.created.isoformat(),
                        "sender": {"uuid": initiator_uuid},
                        "addresseeCount": 1,
                        "subject": {"uuid": break_uuid},
                    },
                    "participants": {
                        "count": 1,
                        "edges": [{"node": {"uuid": initiator_uuid}}],
                    },
                },
                "success": True,
                "errors": None,
            }
        }
    }


def test_initiate_break_returns_created_break(client_query, friend, user, auth_headers):
    """Should return the created break."""
    response = client_query(INITIATE_BREAK_MUTATION, headers=auth_headers)
    content = response.json()  # object_hook=lambda d: SimpleNamespace(**d)

    actual_break = user.breaks.single()
    expected = expected_initiate_break_response(actual_break, user)

    assert content == expected


def test_initiate_break_with_variables_returns_created_break(
    client_query, friend, user, auth_headers
):
    """Should return the created break."""
    start_time = timezone.now() + timedelta(hours=1)
    variables = {"addressees": [str(friend.uuid)], "startTime": start_time.isoformat()}

    response = client_query(
        INITIATE_BREAK_MUTATION, variables=variables, headers=auth_headers
    )
    content = response.json()

    actual_break = user.breaks.single()
    expected = expected_initiate_break_response(actual_break, user)

    assert content == expected


def test_initiate_break_when_unauthenticated_fails(snapshot, client_query):
    """An unauthenticated user should not be able to initiate a break."""
    response = client_query(INITIATE_BREAK_MUTATION)
    content = response.json()

    snapshot.assert_match(content)


def test_accept_break_invitation_when_invitation_exists(
    client_query, user, friend, auth_headers
):
    """Should accept and return the invitation along with the break."""
    pass
