from django.utils.translation import gettext as _

from kaffepause.common.exceptions import DefaultError


class LocationDoesNotExist(DefaultError):
    default_message = _("Location with this id does not exist.")
