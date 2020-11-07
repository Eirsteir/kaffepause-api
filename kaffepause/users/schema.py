import uuid

import graphene
from django.contrib.auth import get_user_model
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from kaffepause.friendships.models import Friendship, FriendshipStatus
from kaffepause.friendships.selectors import get_friends
from kaffepause.friendships.services import create_friendship

User = get_user_model()


class UUIDNode(
    relay.Node
):  # extends graphene.relay.Node and returns a non-encoded ID
    class Meta:
        name = "UUIDNode"

    @staticmethod
    def to_global_id(type, id):
        return id


class UserNode(DjangoObjectType):
    class Meta:
        model = User
        fields = (
            "id",
            "name",
            "username",
            "friends",
        )
        filter_fields = {
            "id": ["exact"],
            "name": ["exact", "icontains", "istartswith"],
            "username": ["exact", "icontains", "istartswith"],
            "friends": ["exact"],
            "friends__name": ["exact"],
        }
        interfaces = (UUIDNode,)

    def resolve_friends(parent, info):

        return get_friends(parent)


class FriendshipNode(DjangoObjectType):
    class Meta:
        model = Friendship
        filter_fields = ("from_user", "to_user", "status", "since")
        interfaces = (relay.Node,)


class FriendshipStatusNode(DjangoObjectType):
    class Meta:
        model = FriendshipStatus
        filter_fields = ("name", "verb", "from_slug", "to_slug", "slug")
        interfaces = (relay.Node,)


class Query(graphene.ObjectType):
    user = relay.Node.Field(UserNode)
    all_users = DjangoFilterConnectionField(UserNode)

    friendships = relay.Node.Field(FriendshipNode)
    all_friendships = DjangoFilterConnectionField(FriendshipNode)

    def resolve_all_users(root, info):
        return User.objects.all()


class SendFriendRequest(graphene.Mutation):
    class Arguments:
        to_friend = graphene.String()

    # This defines the response of the mutation
    friendship = graphene.Field(FriendshipNode)
    ok = graphene.Boolean()

    def mutate(self, info, to_friend):
        current_user = info.context.user
        to_friend = User.objects.get(id=to_friend)
        friendship = create_friendship(
            from_user=current_user, to_user=to_friend
        )
        return SendFriendRequest(friendship=friendship, ok=True)


class Mutation:

    send_friend_request = SendFriendRequest.Field()
