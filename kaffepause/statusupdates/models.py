from neomodel import RelationshipTo, StringProperty

from kaffepause.common.enums import STATUS_UPDATE
from kaffepause.common.models import TimeStampedNode
from kaffepause.statusupdates.enums import StatusUpdateRelationship, StatusUpdateType


class StatusUpdate(TimeStampedNode):
    type = StringProperty(required=True, choices=StatusUpdateType.choices())
    previous = RelationshipTo(STATUS_UPDATE, StatusUpdateRelationship.PREVIOUS)