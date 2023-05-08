from django.utils.translation import gettext as _

from kaffepause.common.exceptions import DefaultError


class GroupDoesNotExist(DefaultError):
    default_message = _("Could not find a group with this id")


class EmptyGroupError(DefaultError):
    default_message = _("Gruppen må ha medlemmer.")


class CannotLeaveGroupWhenSingleMember(DefaultError):
    default_message = _("Du kan ikke forlate gruppen når du er eneste medlem. Du kan kun slette den.")
