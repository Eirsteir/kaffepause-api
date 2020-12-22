import graphene
from graphene import relay

from kaffepause.common.types import CountableConnection
from kaffepause.relationships.selectors import (
    get_friends,
    get_friendship_status,
    get_social_context_between,
)
from kaffepause.statusupdates.types import StatusUpdateNode
from kaffepause.users.selectors import get_user_from_account


# TODO: Lot of repeated logic and fetching in the resolvers - dataLoader?
# https://docs.graphene-python.org/en/latest/execution/dataloader/#dataloader
class UserNode(graphene.ObjectType):
    class Meta:
        interfaces = (relay.Node,)
        name = "User"

    uuid = graphene.UUID()
    name = graphene.String()
    # Short name
    username = graphene.String()
    is_viewer_friend = graphene.Boolean()
    friends = relay.ConnectionField(lambda: UserConnection)
    social_context = graphene.String()
    current_status = graphene.Field(StatusUpdateNode)
    friendship_status = graphene.String()

    def resolve_is_viewer_friend(parent, info):
        current_user_account = info.context.user
        current_user = get_user_from_account(current_user_account)
        return current_user.is_friends_with(parent)

    def resolve_friendship_status(parent, info):
        current_user_account = info.context.user
        current_user = get_user_from_account(current_user_account)
        return get_friendship_status(actor=current_user, user=parent)

    def resolve_friends(parent, info):
        return get_friends(parent)

    def resolve_social_context(parent, info):
        current_user_account = info.context.user
        current_user = get_user_from_account(current_user_account)
        return get_social_context_between(actor=current_user, other=parent)

    def resolve_current_status(parent, info):
        current_user_account = info.context.user
        current_user = get_user_from_account(current_user_account)

        if current_user.is_friends_with(parent):
            return parent.get_current_status()

        return None


class UserConnection(CountableConnection):
    class Meta:
        node = UserNode
