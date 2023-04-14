from django.utils.translation import gettext_lazy as _

from kaffepause.common.exceptions import DefaultError


class InvitationExpired(DefaultError):
    default_message = _("Invitasjonen er utgått.")


class AlreadyReplied(DefaultError):
    default_message = _("Du har allerede svart på invitasjonen.")


class BreakInvitationExpiresBeforeStartTime(DefaultError):
    default_message = _(
        "Invitasjonen kan ikke utgå før pausen skal starte"
    )


class InvalidInvitationExpiration(DefaultError):
    default_message = _("The invitation expiration is invalid")


class InvalidInvitationUpdate(DefaultError):
    default_message = _("Kunne ikke oppdatere invitasjonen")


class InvalidBreakStartTime(DefaultError):
    default_message = _("Pausen må begynne i fremtiden.")


class InvitationNotAddressedAtUser(DefaultError):
    default_message = _("Denne invitasjonen er ikke rettet mot denne brukeren.")
