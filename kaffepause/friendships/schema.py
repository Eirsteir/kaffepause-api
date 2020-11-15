import graphene
from django.contrib.auth import get_user_model
from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField

from kaffepause.friendships.mutations import (
    AcceptFriendRequest,
    CancelFriendRequest,
    SendFriendRequest,
    UnfriendUser,
)
from kaffepause.friendships.selectors import (
    get_friends,
    get_incoming_requests,
    get_outgoing_requests,
)
from kaffepause.friendships.types import FriendshipNode
from kaffepause.users.schema import User

UserModel = get_user_model()


class Query(graphene.ObjectType):

    friendship = relay.Node.Field(FriendshipNode)
    # Get all friends of the user
    all_friendships = DjangoFilterConnectionField(User, user=graphene.String())
    friending_possibilities = DjangoFilterConnectionField(User)
    outgoing_friend_requests = DjangoFilterConnectionField(User)

    def resolve_all_friendships(root, info, user):
        user = UserModel.objects.get(id=user)
        return get_friends(user)

    def resolve_friending_possibilities(root, info):
        user = info.context.user
        return get_incoming_requests(user)

    def resolve_outgoing_friend_requests(root, info):
        user = info.context.user
        return get_outgoing_requests(user)


class Mutation(graphene.ObjectType):

    send_friend_request = SendFriendRequest.Field()
    cancel_friend_request = CancelFriendRequest.Field()
    accept_friend_request = AcceptFriendRequest.Field()
    unfriend_user = UnfriendUser.Field()
