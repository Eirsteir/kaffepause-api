import graphene
from django.contrib.auth import get_user_model
from graphql_auth.schema import UserNode

from kaffepause.common.schema import Output
from kaffepause.friendships.services import (
    accept_friend_request,
    delete_friendship,
    send_friend_request,
)
from kaffepause.friendships.types import FriendshipNode
from kaffepause.users.schema import User

UserModel = get_user_model()


class SendFriendRequest(Output, graphene.Mutation):
    class Arguments:
        to_friend = graphene.String()

    # This defines the response of the mutation
    friendship = graphene.Field(User)
    ok = graphene.Boolean(default_value=False)

    def mutate(self, info, to_friend):
        current_user = info.context.user
        to_friend = UserModel.objects.get(id=to_friend)
        friendship = send_friend_request(actor=current_user, to_user=to_friend)
        to_user = friendship.to_user
        return SendFriendRequest(friendship=to_user, ok=True)


class CancelFriendRequest(Output, graphene.Mutation):
    class Arguments:
        to_friend = graphene.String()

    # This defines the response of the mutation
    cancelled_friend_requestee = graphene.Field(UserNode)
    ok = graphene.Boolean(default_value=False)

    def mutate(self, info, to_friend):
        current_user = info.context.user
        to_friend = UserModel.objects.get(id=to_friend)
        delete_friendship(actor=current_user, user=to_friend)

        return CancelFriendRequest(cancelled_friend_requestee=to_friend, ok=True)


class UnfriendUser(Output, graphene.Mutation):
    class Arguments:
        friend = graphene.String()

    unfriended_user = graphene.Field(UserNode)
    ok = graphene.Boolean(default_value=False)

    def mutate(self, info, friend):
        current_user = info.context.user
        friend = UserModel.objects.get(id=friend)
        delete_friendship(actor=current_user, user=friend)

        return UnfriendUser(unfriended_user=friend, ok=True)


class AcceptFriendRequest(Output, graphene.Mutation):
    class Arguments:
        from_user = graphene.String()

    # This defines the response of the mutation
    friendship = graphene.Field(FriendshipNode)
    ok = graphene.Boolean(default_value=False)

    def mutate(self, info, from_user):
        current_user = info.context.user
        from_user = UserModel.objects.get(id=from_user)
        friendship = accept_friend_request(actor=current_user, from_user=from_user)

        return AcceptFriendRequest(friendship=friendship, ok=True)


class BlockUser(graphene.Mutation):
    class Arguments:
        user = graphene.String()

    pass


class UnblockUser(graphene.Mutation):
    class Arguments:
        user = graphene.String()

    pass
