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
    latitude = graphene.Float()
    longitude = graphene.Float()

    def resolve_status_type(parent, info):
        return StatusUpdateType[parent.status_type].name

    def resolve_verb(parent, info):
        return StatusUpdateType[parent.status_type].value

    def resolve_latitude(parent, info):
        print(parent.geo_location)
        print(parent.geo_location.__dict__)

        return parent.latitude

    def resolve_longitude(parent, info):
        return parent.longitude