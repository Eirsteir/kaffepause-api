import graphene
from graphene import relay

from kaffepause.common.types import CountableConnection
from kaffepause.relationships.selectors import (
    get_friends,
    get_friends_count,
    get_friendship_status,
    get_social_context_between,
)
from kaffepause.statusupdates.types import StatusUpdateNode
from kaffepause.users.selectors import get_user_from_account


class UserNode(graphene.ObjectType):
    class Meta:
        interfaces = (relay.Node,)
        name = "User"

    uuid = graphene.String()
    name = graphene.String()
    username = graphene.String()
    friends_count = graphene.Int()
    friends = relay.ConnectionField(lambda: UserConnection)
    social_context = graphene.String()
    current_status = graphene.Field(StatusUpdateNode)
    friendship_status = graphene.String()

    def resolve_uuid(parent, info):
        return parent.uuid

    def resolve_friendship_status(parent, info):
        current_user_account = info.context.user
        current_user = get_user_from_account(current_user_account)
        return get_friendship_status(actor=current_user, user=parent)

    def resolve_friends_count(parent, info):
        return get_friends_count(parent)

    def resolve_friends(parent, info):
        return get_friends(parent)

    def resolve_social_context(parent, info):
        current_user_account = info.context.user
        current_user = get_user_from_account(current_user_account)
        return get_social_context_between(actor=current_user, other=parent)

    def resolve_current_status(parent, info):
        # TODO: only for followers

        return parent.current_status.single()


class UserConnection(CountableConnection):
    class Meta:
        node = UserNode
