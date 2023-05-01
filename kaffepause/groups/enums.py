from django.utils.translation import gettext as _

from kaffepause.common.bases import NeomodelRelationshipEnum


class GroupRelationship(NeomodelRelationshipEnum):
    HAS_MEMBER = _("Has member")
