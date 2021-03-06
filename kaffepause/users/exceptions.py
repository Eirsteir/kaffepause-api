from django.utils.translation import gettext as _

from kaffepause.common.exceptions import DefaultError


class UsernameAlreadyInUse(DefaultError):
    default_message = _("A user with this username already exists")


class UserDoesNotExist(DefaultError):
    default_message = _("Could not find a user with this id")
