import graphene
from graphene import relay

from kaffepause.statusupdates.enums import StatusUpdateType


class StatusUpdateNode(graphene.ObjectType):
    class Meta:
        interfaces = (relay.Node,)
        name = "StatusUpdate"

    status_type = graphene.String()
    verb = graphene.String()
    created = graphene.DateTime()

    def resolve_status_type(parent, info):
        print(parent.status_type)
        return StatusUpdateType[parent.status_type].name

    def resolve_verb(parent, info):
        return StatusUpdateType[parent.status_type].value
