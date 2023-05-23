from django.utils.translation import gettext_lazy as _

from kaffepause.common.bases import NeomodelRelationshipEnum


class AccountRelationship(NeomodelRelationshipEnum):
    HAS_ACCOUNT = _("Has account")
    HAS_SESSION = _("Has session")

