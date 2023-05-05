import graphene
from graphene import relay

from kaffepause.common.types import CountableConnection
import kaffepause.groups.types
from kaffepause.location.types import LocationNode
from kaffepause.relationships.selectors import (
    get_friends,
    get_friendship_status,
    get_social_context_between,
)
from kaffepause.statusupdates.types import StatusUpdateNode
from kaffepause.users.selectors import get_user, get_user_from_account


# TODO: Lot of repeated logic and fetching in the resolvers - dataLoader?
# https://docs.graphene-python.org/en/latest/execution/dataloader/#dataloader
class UserNode(graphene.ObjectType):
    class Meta:
        interfaces = (relay.Node,)
        name = "User"

    uuid = graphene.UUID()
    name = graphene.String()
    short_name = graphene.String()
    locale = graphene.String()
    profile_pic = graphene.String()
    username = graphene.String()
    is_viewer_friend = graphene.Boolean()
    friends = relay.ConnectionField(lambda: UserConnection)
    social_context = graphene.String()
    current_status = graphene.Field(StatusUpdateNode)
    friendship_status = graphene.String()
    preferred_location = graphene.Field(LocationNode)
    current_location = graphene.Field(LocationNode)
    groups = graphene.List(lambda: kaffepause.groups.types.GroupNode)

    def resolve_short_name(parent, info):
        return parent.short_name

    def resolve_is_viewer_friend(parent, info):
        current_user_account = info.context.user
        current_user = get_user_from_account(account=current_user_account)
        subject = get_user(user_uuid=parent.uuid)
        return current_user.is_friends_with(user=subject)

    def resolve_friendship_status(parent, info):
        current_user_account = info.context.user
        current_user = get_user_from_account(account=current_user_account)
        subject = get_user(user_uuid=parent.uuid)
        return get_friendship_status(actor=current_user, user=subject)

    def resolve_friends(parent, info):
        return get_friends(parent)

    def resolve_social_context(parent, info):
        current_user_account = info.context.user
        current_user = get_user_from_account(account=current_user_account)
        subject = get_user(user_uuid=parent.uuid)
        return get_social_context_between(actor=current_user, other=subject)

    def resolve_current_status(parent, info):
        current_user_account = info.context.user
        current_user = get_user_from_account(account=current_user_account)
        subject = get_user(user_uuid=parent.uuid)

        if current_user.is_friends_with(subject):
            return subject.get_current_status()

        return None

    def resolve_preferred_location(parent, info):
        return parent.get_preferred_location()

    def resolve_current_location(parent, info):
        return parent.get_current_location()

    def resolve_groups(parent, info):
        return parent.groups.all()


class UserConnection(CountableConnection):
    class Meta:
        node = UserNode
