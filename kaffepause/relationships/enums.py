from django.utils.translation import gettext_lazy as _

from kaffepause.common.bases import NeomodelRelationshipEnum


class UserRelationship(NeomodelRelationshipEnum):
    ARE_FRIENDS = _("Are friends")
    REQUESTING_FRIENDSHIP = _("Requested")
    FOLLOWING = _("Following")


class NonRelatedRelationship(NeomodelRelationshipEnum):
    CAN_REQUEST = _("Can request")
    CANNOT_REQUEST = _("Cannot request")
    OUTGOING_REQUEST = _("Outgoing request")
    INCOMING_REQUEST = _("Incoming request")
