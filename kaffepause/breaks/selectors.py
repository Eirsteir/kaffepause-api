from django.contrib.auth import get_user_model

from kaffepause.breaks.models import BreakInvitation
from kaffepause.common.typing import QuerySet

User = get_user_model()


def get_pending_break_invitations(actor: User) -> QuerySet[BreakInvitation]:
    """Returns all non-expired break invitations awaiting reply."""
    pass
