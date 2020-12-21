import graphene
from graphene import relay

from kaffepause.relationships.mutations import (
    AcceptFriendRequest,
    CancelFriendRequest,
    FollowFriend,
    SendFriendRequest,
    UnfollowFriend,
    UnfriendUser,
)
from kaffepause.relationships.selectors import (
    get_friends,
    get_incoming_requests,
    get_outgoing_requests,
)
from kaffepause.users.models import User
from kaffepause.users.selectors import get_user_from_account
from kaffepause.users.types import UserConnection


class Query(graphene.ObjectType):

    friendships = relay.ConnectionField(UserConnection, user=graphene.String())
    friending_possibilities = relay.ConnectionField(UserConnection)
    outgoing_friend_requests = relay.ConnectionField(UserConnection)

    def resolve_all_relationships(root, info, user):
        user = User.nodes.get(uuid=user)
        return get_friends(user)

    def resolve_friending_possibilities(root, info):
        account = root._get_account(info)
        user = get_user_from_account(account)
        return get_incoming_requests(user)

    def resolve_outgoing_friend_requests(root, info):
        account = root._get_account(info)
        user = get_user_from_account(account)
        return get_outgoing_requests(user)

    def _get_account(self, info):
        return info.context.user


class Mutation(graphene.ObjectType):

    send_friend_request = SendFriendRequest.Field()
    cancel_friend_request = CancelFriendRequest.Field()
    accept_friend_request = AcceptFriendRequest.Field()
    unfriend_user = UnfriendUser.Field()
    unfollow_friend = UnfollowFriend.Field()
    follow_friend = FollowFriend.Field()
