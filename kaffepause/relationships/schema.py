import graphene
from graphene import relay

from kaffepause.common.bases import NeomodelGraphQLMixin
from kaffepause.common.decorators import login_required
from kaffepause.relationships.mutations import (
    AcceptFriendRequest,
    CancelFriendRequest,
    FollowFriend,
    RejectFriendRequest,
    SendFriendRequest,
    UnfollowFriend,
    UnfriendUser,
)
from kaffepause.relationships.selectors import (
    get_friends,
    get_incoming_requests,
    get_outgoing_requests, get_friend_recommendations,
)
from kaffepause.users.models import User
from kaffepause.users.selectors import get_user_from_account
from kaffepause.users.types import UserConnection


class Query(NeomodelGraphQLMixin, graphene.ObjectType):

    friendships = relay.ConnectionField(UserConnection, user=graphene.String())
    friending_possibilities = relay.ConnectionField(UserConnection)
    outgoing_friend_requests = relay.ConnectionField(UserConnection)
    friend_recommendations = relay.ConnectionField(UserConnection)

    @classmethod
    @login_required
    def resolve_relationships(cls, root, info, user):
        user = User.nodes.get(uuid=user)
        return get_friends(user)

    @classmethod
    @login_required
    def resolve_friending_possibilities(cls, root, info):
        user = cls.get_current_user()
        return get_incoming_requests(user)

    @classmethod
    @login_required
    def resolve_outgoing_friend_requests(cls, root, info):
        user = cls.get_current_user()
        return get_outgoing_requests(user)

    @classmethod
    @login_required
    def resolve_friend_recommendations(cls, root, info):
        user = cls.get_current_user()
        return get_friend_recommendations(user, limit=10)


class Mutation(graphene.ObjectType):

    send_friend_request = SendFriendRequest.Field()
    cancel_friend_request = CancelFriendRequest.Field()
    accept_friend_request = AcceptFriendRequest.Field()
    reject_friend_request = RejectFriendRequest.Field()
    unfriend_user = UnfriendUser.Field()
    unfollow_friend = UnfollowFriend.Field()
    follow_friend = FollowFriend.Field()
