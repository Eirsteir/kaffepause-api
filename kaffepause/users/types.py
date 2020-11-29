import graphene
from graphene import relay

from kaffepause.relationships.selectors import (
    get_friends,
    get_friends_count,
    get_social_context_between,
)
from kaffepause.users.schema import UserConnection
from kaffepause.users.selectors import get_user_from_account


class UserType(graphene.ObjectType):
    class Meta:
        interfaces = (relay.Node,)
        name = "user"

    uid = graphene.UUID()
    name = graphene.String()

    def resolve_uid(parent, info):
        return parent.uid

    def resolve_name(parent, info):
        return parent.name

    friends_count = graphene.Int()
    friends = relay.Connection(UserConnection)
    # profile_action = graphene.Field(ProfileAction)

    # friendship_status = graphene.String()
    social_context = graphene.String()

    # def resolve_friendship_status(parent, info):
    #     current_user = info.context.user
    #     status = get_friendship_status(actor=current_user, user=parent)
    #     return status.name

    def resolve_friends_count(parent, info):
        return get_friends_count(parent)

    def resolve_friends(parent, info):
        return get_friends(parent)

    def resolve_social_context(parent, info):
        current_user_account = info.context.user
        current_user = get_user_from_account(current_user_account)
        return get_social_context_between(actor=current_user, other=parent)
