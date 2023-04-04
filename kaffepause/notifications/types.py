import graphene
from graphene import relay

from kaffepause.common.types import CountableConnection
from kaffepause.notifications.enums import SeenState
from kaffepause.users.types import UserNode


class NotificationNode(graphene.ObjectType):
    class Meta:
        interfaces = (relay.Node,)
        name = "Notification"

    uuid = graphene.UUID()
    seen_state = graphene.String()
    entity_type = graphene.String()
    entity_id = graphene.String()
    text = graphene.String()
    url = graphene.String()
    actor = graphene.Field(UserNode)

    def resolve_seen_state(parent, info):
        return SeenState[parent.seen_state].name

    def resolve_url(parent, info):
        return parent.url

    def resolve_actor(parent, info):
        return parent.actor.single()


class NotificationConnection(relay.Connection):
    class Meta:
        node = NotificationNode
