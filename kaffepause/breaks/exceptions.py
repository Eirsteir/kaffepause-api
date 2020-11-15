from django.utils.translation import gettext_lazy as _

from kaffepause.common.exceptions import DefaultError


class InvitationExpired(DefaultError):
    default_message = _("Invitation has expired")


class AlreadyReplied(DefaultError):
    default_message = _("Invitation has already been replied to")


class BreakInvitationExpiresBeforeStartTime(DefaultError):
    default_message = _(
        "The invitation cannot expire before the break is supposed to start"
    )


class InvalidInvitationExpiration(DefaultError):
    default_message = _("The invitation expiration is invalid")


class InvalidInvitationUpdate(DefaultError):
    default_message = _("Cannot update invitation")
