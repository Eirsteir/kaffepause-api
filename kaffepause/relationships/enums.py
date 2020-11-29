from enum import Enum

from django.utils.translation import gettext_lazy as _


class UserRelationship(Enum):
    ARE_FRIENDS = _("Are friends")
    REQUESTING_FRIENDSHIP = _("Requested")
    BLOCKING = _("Blocking")

    def __str__(self):
        return self.name


class NonRelatedRelationship(Enum):
    CAN_REQUEST = _("Can request")
    CANNOT_REQUEST = _("Cannot request")

    def __str__(self):
        return self.name


ARE_FRIENDS = UserRelationship.ARE_FRIENDS
REQUESTING_FRIENDSHIP = UserRelationship.REQUESTING_FRIENDSHIP
BLOCKING = UserRelationship.BLOCKING
CAN_REQUEST = NonRelatedRelationship.CAN_REQUEST
CANNOT_REQUEST = NonRelatedRelationship.CANNOT_REQUEST
