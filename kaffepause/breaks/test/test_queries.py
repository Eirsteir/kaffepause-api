import pytest

from kaffepause.breaks.services import create_break_and_invitation
from kaffepause.breaks.test.graphql_requests import PENDING_BREAK_INVITATIONS_QUERY
from kaffepause.users.models import User

pytestmark = pytest.mark.django_db


def test_pending_break_invitations_returns_unanswered_non_expired_invitations(
    client_query, friend, user, auth_headers
):
    """Should return the pending break invitations."""
    # TODO: timezones, the invitation is expired
    break_ = create_break_and_invitation(actor=friend)
    response = client_query(
        PENDING_BREAK_INVITATIONS_QUERY,
        op_name="pendingBreakInvitations",
        headers=auth_headers,
    )
    content = response.json()
    print(content)
    print(break_)

    assert False
