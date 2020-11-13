import graphene
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from graphql_auth.decorators import verification_required
from graphql_auth.schema import UserNode

from kaffepause.common.bases import Output, VerificationRequiredMixin
from kaffepause.friendships.services import (
    accept_friend_request,
    delete_friendship,
    send_friend_request,
)
from kaffepause.friendships.types import FriendshipNode
from kaffepause.users.schema import User

UserModel = get_user_model()


class SendFriendRequest(VerificationRequiredMixin, Output, graphene.Mutation):
    class Arguments:
        to_friend = graphene.String(required=True)

    friendship = graphene.Field(User)

    @classmethod
    def resolve_mutation(cls, root, info, to_friend):
        current_user = info.context.user
        to_friend = UserModel.objects.get(id=to_friend)
        friendship = send_friend_request(actor=current_user, to_user=to_friend)
        to_user = friendship.to_user
        return cls(friendship=to_user)


class CancelFriendRequest(VerificationRequiredMixin, Output, graphene.Mutation):
    class Arguments:
        to_friend = graphene.String(required=True)

    cancelled_friend_requestee = graphene.Field(UserNode)

    @classmethod
    def resolve_mutation(cls, root, info, to_friend):
        current_user = info.context.user
        to_friend = UserModel.objects.get(id=to_friend)
        delete_friendship(actor=current_user, user=to_friend)

        return cls(cancelled_friend_requestee=to_friend)


class UnfriendUser(VerificationRequiredMixin, Output, graphene.Mutation):
    class Arguments:
        friend = graphene.String(required=True)

    unfriended_user = graphene.Field(UserNode)

    @classmethod
    def resolve_mutation(cls, root, info, friend):
        current_user = info.context.user
        friend = UserModel.objects.get(id=friend)
        delete_friendship(actor=current_user, user=friend)

        return cls(unfriended_user=friend)


class AcceptFriendRequest(VerificationRequiredMixin, Output, graphene.Mutation):
    class Arguments:
        from_user = graphene.String(required=True)

    friendship = graphene.Field(FriendshipNode)

    @classmethod
    def resolve_mutation(cls, root, info, from_user):
        current_user = info.context.user
        from_user = UserModel.objects.get(id=from_user)
        friendship = accept_friend_request(actor=current_user, from_user=from_user)

        return cls(friendship=friendship)


class BlockUser(VerificationRequiredMixin, Output, graphene.Mutation):
    class Arguments:
        user = graphene.String(required=True)

    @classmethod
    def resolve_mutation(cls, root, info, user):
        raise NotImplementedError()


class UnblockUser(VerificationRequiredMixin, Output, graphene.Mutation):
    class Arguments:
        user = graphene.String(required=True)

    @classmethod
    def resolve_mutation(cls, root, info, user):
        raise NotImplementedError()
