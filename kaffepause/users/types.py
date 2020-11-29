import graphene
from graphene import relay

from kaffepause.common.types import CountingNodeConnection
from kaffepause.relationships.selectors import (
    get_friends,
    get_friends_count,
    get_social_context_between,
)
from kaffepause.users.selectors import get_user_from_account


class UserNode(graphene.ObjectType):
    class Meta:
        interfaces = (relay.Node,)
        name = "user"

    uid = graphene.UUID()
    name = graphene.String()
    username = graphene.String()
    friends_count = graphene.Int()
    friends = relay.ConnectionField(lambda: UserConnection)
    social_context = graphene.String()

    # friendship_status = graphene.String()

    # def resolve_friendship_status(parent, info):
    #     current_user = info.context.user
    #     status = get_friendship_status(actor=current_user, user=parent)
    #     return status.name

    def resolve_uid(parent, info):
        return parent.uid

    def resolve_name(parent, info):
        return parent.name

    def resolve_username(parent, info):
        return parent.username

    def resolve_friends_count(parent, info):
        return get_friends_count(parent)

    def resolve_friends(parent, info):
        return get_friends(parent)

    def resolve_social_context(parent, info):
        current_user_account = info.context.user
        current_user = get_user_from_account(current_user_account)
        return get_social_context_between(actor=current_user, other=parent)


class UserConnection(CountingNodeConnection):
    class Meta:
        node = UserNode
