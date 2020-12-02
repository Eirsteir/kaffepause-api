from django.utils.translation import gettext_lazy as _

from kaffepause.common.bases import NeomodelRelationshipEnum


class UserRelationship(NeomodelRelationshipEnum):
    ARE_FRIENDS = _("Are friends")
    REQUESTING_FRIENDSHIP = _("Requested")


class NonRelatedRelationship(NeomodelRelationshipEnum):
    CAN_REQUEST = _("Can request")
    CANNOT_REQUEST = _("Cannot request")


ARE_FRIENDS = UserRelationship.ARE_FRIENDS
REQUESTING_FRIENDSHIP = UserRelationship.REQUESTING_FRIENDSHIP
CAN_REQUEST = NonRelatedRelationship.CAN_REQUEST
CANNOT_REQUEST = NonRelatedRelationship.CANNOT_REQUEST
