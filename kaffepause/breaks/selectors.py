from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils import timezone

from kaffepause.breaks.models import BreakInvitation
from kaffepause.common.typing import QuerySet

User = get_user_model()


def get_break_invitations_awaiting_reply(actor: User) -> QuerySet[BreakInvitation]:
    """Returns all non-expired break invitations awaiting reply."""
    query = _get_incoming_query(actor) & Q(reply=None, expiry__gt=timezone.now())
    return BreakInvitation.objects.filter(query)


def get_expired_break_invitations(actor: User) -> QuerySet[BreakInvitation]:
    query = _get_incoming_query(actor) & Q(expiry__lte=timezone.now())
    return BreakInvitation.objects.filter(query)


def get_all_break_invitations(actor: User) -> QuerySet[BreakInvitation]:
    return BreakInvitation.objects.filter(_get_incoming_query(actor))


def _get_incoming_query(user: User) -> Q:
    return Q(recipient=user)


def get_outgoing_break_invitations(actor: User) -> QuerySet[BreakInvitation]:
    return BreakInvitation.objects.filter(sender=actor)
