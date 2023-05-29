import graphene

from kaffepause.common.bases import LoginRequiredMixin, NeomodelGraphQLMixin, Output
from kaffepause.relationships.services import (
    accept_friend_request,
    cancel_friend_request,
    follow_friend,
    reject_friend_request,
    send_friend_request,
    unfollow_friend,
    unfriend_user,
)
from kaffepause.users.models import User
from kaffepause.users.selectors import get_user
from kaffepause.users.types import UserNode


class SendFriendRequest(
    LoginRequiredMixin, Output, graphene.Mutation
):
    class Arguments:
        to_friend = graphene.String(required=True)

    sent_friend_requestee = graphene.Field(UserNode)

    @classmethod
    def resolve_mutation(cls, root, info, to_friend):
        current_user = info.context.user
        to_friend = get_user(uuid=to_friend)
        send_friend_request(actor=current_user, to_user=to_friend)

        return cls(success=True, sent_friend_requestee=to_friend)


class CancelFriendRequest(
    LoginRequiredMixin, Output, graphene.Mutation
):
    class Arguments:
        to_friend = graphene.String(required=True)

    cancelled_friend_requestee = graphene.Field(UserNode)

    @classmethod
    def resolve_mutation(cls, root, info, to_friend):
        current_user = info.context.user
        to_friend = get_user(uuid=to_friend)
        cancel_friend_request(actor=current_user, to_user=to_friend)

        return cls(success=True, cancelled_friend_requestee=to_friend)


class UnfriendUser(LoginRequiredMixin, Output, graphene.Mutation):
    class Arguments:
        friend = graphene.String(required=True)

    unfriended_person = graphene.Field(UserNode)

    @classmethod
    def resolve_mutation(cls, root, info, friend):
        current_user = info.context.user
        friend = get_user(uuid=friend)
        unfriend_user(actor=current_user, friend=friend)

        return cls(success=True, unfriended_person=friend)


class AcceptFriendRequest(
    LoginRequiredMixin, Output, graphene.Mutation
):
    class Arguments:
        requester = graphene.String(required=True)

    friend = graphene.Field(UserNode)

    @classmethod
    def resolve_mutation(cls, root, info, requester):
        current_user = info.context.user
        requester = get_user(uuid=requester)
        accept_friend_request(actor=current_user, requester=requester)

        return cls(success=True, friend=requester)


class RejectFriendRequest(
    LoginRequiredMixin, Output, graphene.Mutation
):
    class Arguments:
        requester = graphene.String(required=True)

    rejected_friend_requestee = graphene.Field(UserNode)

    @classmethod
    def resolve_mutation(cls, root, info, requester):
        current_user = info.context.user
        requester = get_user(uuid=requester)
        reject_friend_request(actor=current_user, requester=requester)

        return cls(success=True, rejected_friend_requestee=requester)


class UnfollowFriend(
    LoginRequiredMixin, Output, graphene.Mutation
):
    class Arguments:
        friend_id = graphene.UUID(required=True)

    unfollowed_friend = graphene.Field(UserNode)

    @classmethod
    def resolve_mutation(cls, root, info, friend_id):
        current_user = info.context.user
        friend = get_user(uuid=friend_id)
        unfollow_friend(actor=current_user, friend=friend)
        return cls(success=True, unfollowed_friend=friend)


class FollowFriend(LoginRequiredMixin, Output, graphene.Mutation):
    class Arguments:
        friend_id = graphene.UUID(required=True)

    followed_friend = graphene.Field(UserNode)

    @classmethod
    def resolve_mutation(cls, root, info, friend_id):
        current_user = info.context.user
        friend = get_user(uuid=friend_id)
        follow_friend(actor=current_user, friend=friend)
        return cls(success=True, followed_friend=friend)
