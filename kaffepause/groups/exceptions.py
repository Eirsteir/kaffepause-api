from django.utils.translation import gettext as _

from kaffepause.common.exceptions import DefaultError


class GroupDoesNotExist(DefaultError):
    default_message = _("Could not find a group with this id")
