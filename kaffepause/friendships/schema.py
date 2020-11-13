import graphene
from django.contrib.auth import get_user_model
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_auth.schema import UserNode

from kaffepause.friendships.models import Friendship, FriendshipStatus
from kaffepause.friendships.selectors import (
    get_friends,
    get_incoming_requests,
    get_outgoing_requests,
)
from kaffepause.friendships.services import accept_friend_request, send_friend_request
from kaffepause.users.schema import ExtendedUserNode

User = get_user_model()


class FriendshipNode(DjangoObjectType):
    class Meta:
        model = Friendship
        filter_fields = {
            "from_user__username": ["exact"],
            "to_user__username": ["exact"],
            "status__name": ["exact"],
        }
        interfaces = (relay.Node,)

    since = graphene.DateTime()

    def resolve_since(self, info):
        return self.since


class FriendshipStatusNode(DjangoObjectType):
    class Meta:
        model = FriendshipStatus
        filter_fields = ("name", "verb", "from_slug", "to_slug", "slug")
        interfaces = (relay.Node,)


class Query(graphene.ObjectType):

    friendship = relay.Node.Field(FriendshipNode)
    # Get all friends of the user
    all_friendships = DjangoFilterConnectionField(
        ExtendedUserNode, user=graphene.String()
    )
    friending_possibilities = DjangoFilterConnectionField(ExtendedUserNode)
    outgoing_friend_requests = DjangoFilterConnectionField(ExtendedUserNode)

    @staticmethod
    def resolve_all_friendships(root, info, user):
        user = User.objects.get(id=user)
        return get_friends(user)

    @staticmethod
    def resolve_friending_possibilities(root, info):
        user = info.context.user
        return get_incoming_requests(user)

    @staticmethod
    def resolve_outgoing_friend_requests(root, info):
        user = info.context.user
        return get_outgoing_requests(user)


class SendFriendRequest(graphene.Mutation):
    class Arguments:
        to_friend = graphene.String()

    # This defines the response of the mutation
    friendship = graphene.Field(ExtendedUserNode)
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
    cancelled_friend_requestee = graphene.Field(UserNode)
    ok = graphene.Boolean(default_value=False)

    def mutate(self, info, to_friend):
        current_user = info.context.user
        to_friend = User.objects.get(id=to_friend)
        friendship = send_friend_request(actor=current_user, to_user=to_friend)

        return SendFriendRequest(cancelled_friend_requestee=friendship.to_user, ok=True)


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
