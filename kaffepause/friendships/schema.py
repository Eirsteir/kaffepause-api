import graphene
from django.contrib.auth import get_user_model
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from kaffepause.friendships.models import Friendship, FriendshipStatus
from kaffepause.friendships.services import (
    accept_friend_request,
    create_friendship,
    send_friend_request,
)
from kaffepause.users.schema import UserNode

User = get_user_model()


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

    friendships = relay.Node.Field(FriendshipNode)
    all_friendships = DjangoFilterConnectionField(FriendshipNode)


# TODO: Use relay? https://www.howtographql.com/graphql-python/9-relay/
class SendFriendRequest(graphene.Mutation):
    class Arguments:
        to_friend = graphene.String()

    # This defines the response of the mutation
    cancelled_friend_requestee = graphene.Field(UserNode)
    ok = graphene.Boolean(default_value=False)

    def mutate(self, info, to_friend):
        current_user = info.context.user
        to_friend = User.objects.get(id=to_friend)
        friendship = send_friend_request(actor=current_user, to_user=to_friend)

        return SendFriendRequest(friendship=friendship, ok=True)


class CancelFriendRequest(graphene.Mutation):
    class Arguments:
        to_friend = graphene.String()

    # This defines the response of the mutation
    friendship = graphene.Field(FriendshipNode)
    ok = graphene.Boolean(default_value=False)

    def mutate(self, info, to_friend):
        current_user = info.context.user
        to_friend = User.objects.get(id=to_friend)
        friendship = send_friend_request(actor=current_user, to_user=to_friend)

        return SendFriendRequest(friendship=friendship, ok=True)


class AcceptFriendRequest(graphene.Mutation):
    class Arguments:
        from_user = graphene.String()

    # This defines the response of the mutation
    friendship = graphene.Field(FriendshipNode)
    ok = graphene.Boolean(default_value=False)

    def mutate(self, info, from_user):
        current_user = info.context.user
        from_user = User.objects.get(id=from_user)
        friendship = accept_friend_request(actor=current_user, from_user=from_user)

        return AcceptFriendRequest(friendship=friendship, ok=True)


class Mutation:

    send_friend_request = SendFriendRequest.Field()
    accept_friend_request = AcceptFriendRequest.Field()
