from django.db.models import Q

from kaffepause.breaks.models import BreakInvitation
from kaffepause.common.typing import QuerySet
from kaffepause.users.models import User


def get_break_invitations_awaiting_reply(actor: User) -> QuerySet[BreakInvitation]:
    """Returns all non-expired break invitations awaiting reply."""
    raise NotImplementedError


def get_expired_break_invitations(actor: User) -> QuerySet[BreakInvitation]:
    raise NotImplementedError


def get_all_break_invitations(actor: User) -> QuerySet[BreakInvitation]:
    raise NotImplementedError


def _get_incoming_query(user: User) -> Q:
    raise NotImplementedError


def get_outgoing_break_invitations(actor: User) -> QuerySet[BreakInvitation]:
    raise NotImplementedError
