from datetime import timedelta
from uuid import UUID

import pytest
from django.utils import timezone

from kaffepause.breaks.services import create_break_and_invitation
from kaffepause.breaks.test.graphql_requests import (
    ACCEPT_BREAK_INVITATION_MUTATION,
    DECLINE_BREAK_INVITATION_MUTATION,
    INITIATE_BREAK_MUTATION,
)

pytestmark = pytest.mark.django_db


@pytest.fixture
def invitation(friend):
    break_ = create_break_and_invitation(actor=friend)
    return break_.get_invitation()


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


@pytest.fixture
def invitation_action_response(invitation):
    def func(**kwargs):
        action = kwargs.get("action")
        return __invitation_action_response(action, invitation)

    return func


def __invitation_action_response(action, invitation):
    invitation_uuid = str(UUID(invitation.uuid))
    break_uuid = str(UUID(invitation.get_subject().uuid))
    sender_uuid = str(invitation.get_sender().uuid)
    return {
        "data": {
            action: {
                "invitation": {
                    "uuid": invitation_uuid,
                    "created": invitation.created.isoformat(),
                    "sender": {"uuid": sender_uuid},
                    "addresseeCount": 1,
                    "subject": {"uuid": break_uuid},
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


def test_accept_break_invitation_when_invitation_exists_adds_user_to_break_participants_and_invitation_acceptees(
    client_query, user, invitation, auth_headers
):
    """Should accept the invitation by adding the user to list of acceptees and break participants."""
    variables = {"invitation": invitation.uuid}
    client_query(
        ACCEPT_BREAK_INVITATION_MUTATION,
        op_name="acceptBreakInvitation",
        variables=variables,
        headers=auth_headers,
    )

    break_ = invitation.get_subject()

    assert user.breaks.is_connected(break_)
    assert invitation.acceptees.is_connected(user)


def test_accept_break_invitation_when_invitation_exists_returns_invitation(
    client_query, invitation, auth_headers, invitation_action_response
):
    """Should return the accepted invitation."""
    variables = {"invitation": invitation.uuid}
    response = client_query(
        ACCEPT_BREAK_INVITATION_MUTATION,
        op_name="acceptBreakInvitation",
        variables=variables,
        headers=auth_headers,
    )
    content = response.json()
    expected = invitation_action_response(action="acceptBreakInvitation")

    assert content == expected


def test_accept_break_invitation_when_unauthenticated_fails(
    snapshot, client_query, invitation
):
    """Should fail when the user is unauthenticated."""
    variables = {"invitation": invitation.uuid}
    response = client_query(
        ACCEPT_BREAK_INVITATION_MUTATION,
        op_name="acceptBreakInvitation",
        variables=variables,
    )
    content = response.json()

    snapshot.assert_match(content)


def test_decline_break_invitation_when_invitation_exists_adds_user_to_invitation_declineees(
    client_query, user, invitation, auth_headers
):
    """Should decline the invitation by adding the user to list of declineees but not break participants."""
    variables = {"invitation": invitation.uuid}
    client_query(
        DECLINE_BREAK_INVITATION_MUTATION,
        op_name="declineBreakInvitation",
        variables=variables,
        headers=auth_headers,
    )

    assert invitation.declinees.is_connected(user)


def test_decline_break_invitation_when_invitation_exists_returns_invitation(
    client_query, invitation, invitation_action_response, auth_headers
):
    """Should return the declined invitation."""
    variables = {"invitation": invitation.uuid}
    response = client_query(
        DECLINE_BREAK_INVITATION_MUTATION,
        op_name="declineBreakInvitation",
        variables=variables,
        headers=auth_headers,
    )
    content = response.json()
    expected = invitation_action_response(action="declineBreakInvitation")

    assert content == expected


def test_decline_break_invitation_when_unauthenticated_fails(
    snapshot, client_query, invitation
):
    """Should fail when the user is unauthenticated."""
    variables = {"invitation": invitation.uuid}
    response = client_query(
        DECLINE_BREAK_INVITATION_MUTATION,
        op_name="declineBreakInvitation",
        variables=variables,
    )
    content = response.json()

    snapshot.assert_match(content)
