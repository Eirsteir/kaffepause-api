from django.utils.translation import gettext_lazy as _

from kaffepause.common.exceptions import DefaultError


class InvitationExpired(DefaultError):
    default_message = _("Invitation has expired")


class BreakInvitationExpiresBeforeStartTime(DefaultError):
    default_message = _(
        "The invitation cannot expire before the break is supposed to start"
    )
