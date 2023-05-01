from django.utils.translation import gettext as _

from kaffepause.common.bases import NeomodelRelationshipEnum


class GroupRelationship(NeomodelRelationshipEnum):
    CREATED_GROUP = _("Created group")
    HAS_MEMBER = _("Has member")
