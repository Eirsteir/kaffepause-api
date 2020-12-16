from datetime import timedelta
from unittest.mock import patch

import pytest
from django.utils import timezone

from kaffepause.breaks.services import create_break_and_invitation
from kaffepause.breaks.test.graphql_requests import (
    ALL_BREAK_INVITATIONS_QUERY,
    EXPIRED_BREAK_INVITATIONS_QUERY,
    PENDING_BREAK_INVITATIONS_QUERY,
)
from kaffepause.common.utils import time_from_now

pytestmark = pytest.mark.django_db


def test_pending_break_invitations_returns_unanswered_non_expired_invitations(
    client_query, friend, user, auth_headers
):
    """Should return the pending break invitations."""
    break_ = create_break_and_invitation(actor=friend)

    response = client_query(
        PENDING_BREAK_INVITATIONS_QUERY,
        op_name="pendingBreakInvitations",
        headers=auth_headers,
    )
    content = response.json()
    data = content.get("data").get("pendingBreakInvitations")
    actual_invitations = data.get("edges")[0].get("node")

    assert data.get("count") == 1
    assert actual_invitations.get("sender").get("uuid") == friend.uuid
    assert actual_invitations.get("addresseeCount") == 1
    assert actual_invitations.get("subject").get("uuid") == break_.uuid


def test_pending_break_invitations_unauthenticated_returns_error(
    snapshot, client_query
):
    """A user should not be able to retrieve their pending invitations when unauthenticated."""
    response = client_query(
        PENDING_BREAK_INVITATIONS_QUERY,
        op_name="pendingBreakInvitations",
    )
    content = response.json()

    snapshot.assert_match(content)


def test_all_break_invitations_returns_all_break_invitations(
    client_query, friend, auth_headers
):
    """Should return all break invitations."""
    break_ = create_break_and_invitation(actor=friend)

    response = client_query(
        ALL_BREAK_INVITATIONS_QUERY,
        op_name="allBreakInvitations",
        headers=auth_headers,
    )
    content = response.json()
    data = content.get("data").get("allBreakInvitations")
    actual_invitations = data.get("edges")[0].get("node")

    assert data.get("count") == 1
    assert actual_invitations.get("sender").get("uuid") == friend.uuid
    assert actual_invitations.get("addresseeCount") == 1
    assert actual_invitations.get("subject").get("uuid") == break_.uuid


def test_all_break_invitations_unauthenticated(snapshot, client_query):
    """A user should not be able to retrieve their break invitations when unauthenticated."""
    response = client_query(
        ALL_BREAK_INVITATIONS_QUERY,
        op_name="allBreakInvitations",
    )
    content = response.json()

    snapshot.assert_match(content)


@patch("kaffepause.breaks.models.Break.clean")
def test_expired_break_invitations_returns_all_expired_break_invitations(
    mock_clean, client_query, friend, auth_headers
):
    """Should return all break invitations."""

    start_time = timezone.now() + timedelta(hours=-1)
    expired_break = create_break_and_invitation(actor=friend, start_time=start_time)
    create_break_and_invitation(actor=friend)

    response = client_query(
        EXPIRED_BREAK_INVITATIONS_QUERY,
        op_name="expiredBreakInvitations",
        headers=auth_headers,
    )
    content = response.json()
    data = content.get("data").get("expiredBreakInvitations")
    actual_invitations = data.get("edges")[0].get("node")

    assert data.get("count") == 1
    assert actual_invitations.get("sender").get("uuid") == friend.uuid
    assert actual_invitations.get("addresseeCount") == 1
    assert actual_invitations.get("subject").get("uuid") == expired_break.uuid


def test_expired_break_invitations_unauthenticated(snapshot, client_query):
    """A user should not be able to retrieve their expired break invitations when unauthenticated."""
    response = client_query(
        EXPIRED_BREAK_INVITATIONS_QUERY,
        op_name="expiredBreakInvitations",
    )
    content = response.json()

    snapshot.assert_match(content)
