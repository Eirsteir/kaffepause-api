import graphene
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from graphene import relay
from graphql_auth.schema import UserNode
from graphql_auth.settings import graphql_auth_settings

from kaffepause.common.bases import UUIDNode
from kaffepause.common.types import CountingNodeConnection
from kaffepause.friendships.selectors import (
    get_friends,
    get_friendship_status,
    get_mutual_friends,
)
from kaffepause.users.models import User


class UserType(graphene.ObjectType):
    class Meta:
        interfaces = (relay.Node,)

    uid = graphene.UUID()
    name = graphene.String()

    def resolve_uid(parent, info):
        return parent.uid

    def resolve_name(parent, info):
        return parent.name

    # friends_count = graphene.List(UserNode)
    #
    # # profile_action = graphene.Field(ProfileAction)
    #
    # friendship_status = graphene.String()
    # social_context = graphene.String()
    #
    # def resolve_friendship_status(parent, info):
    #     current_user = info.context.user
    #     status = get_friendship_status(actor=current_user, user=parent)
    #     return status.name
    #
    # def resolve_friends_count(parent, info):
    #
    #     return get_friends(parent).count()
    #
    # def resolve_social_context(parent, info):
    #     current_user = info.context.user
    #     mutual_friends = get_mutual_friends(actor=current_user, user=parent)
    #     mutual_friends_count = mutual_friends.count()
    #     return _(f"{mutual_friends_count} mutual friends")


class UserConnection(CountingNodeConnection, relay.Connection):
    class Meta:
        node = UserType
