import graphene
from graphene import relay

from kaffepause.statusupdates.enums import StatusUpdateType


class StatusUpdateNode(graphene.ObjectType):
    class Meta:
        interfaces = (relay.Node,)
        name = "StatusUpdate"

    type = graphene.Enum.from_enum(StatusUpdateType)
    verb = graphene.String()
    created = graphene.DateTime()

    def resolve_verb(parent, info):
        return parent.type.value
