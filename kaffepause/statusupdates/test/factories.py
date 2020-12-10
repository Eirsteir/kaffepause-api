import factory

from kaffepause.common.bases import NeomodelFactory
from kaffepause.statusupdates.enums import StatusUpdateType
from kaffepause.statusupdates.models import StatusUpdate

CHOICES = (field for field, member in StatusUpdateType.__members__.items())


class StatusUpdateFactory(NeomodelFactory):
    class Meta:
        model = StatusUpdate

    status_type = factory.Iterator(CHOICES)
