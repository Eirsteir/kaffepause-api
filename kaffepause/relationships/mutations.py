import graphene

from kaffepause.common.bases import LoginRequiredMixin, NeomodelGraphQLMixin, Output
from kaffepause.relationships.exceptions import RelationshipAlreadyExists
from kaffepause.relationships.services import (
    accept_friend_request,
    cancel_friend_request,
    send_friend_request,
    unfriend_user,
)
from kaffepause.users.models import User
from kaffepause.users.types import UserNode


class SendFriendRequest(
    LoginRequiredMixin, NeomodelGraphQLMixin, Output, graphene.Mutation
):
    class Arguments:
        to_friend = graphene.String(required=True)

    sent_friend_requestee = graphene.Field(UserNode)

    @classmethod
    def resolve_mutation(cls, root, info, to_friend):
        current_user = cls.get_current_user()
        to_friend = User.nodes.get(uid=to_friend)
        send_friend_request(actor=current_user, to_user=to_friend)

        return cls(success=True, sent_friend_requestee=to_friend)


class CancelFriendRequest(
    LoginRequiredMixin, NeomodelGraphQLMixin, Output, graphene.Mutation
):
    class Arguments:
        to_friend = graphene.String(required=True)

    cancelled_friend_requestee = graphene.Field(UserNode)

    @classmethod
    def resolve_mutation(cls, root, info, to_friend):
        current_user = cls.get_current_user()
        to_friend = User.nodes.get(uid=to_friend)
        cancel_friend_request(actor=current_user, to_user=to_friend)

        return cls(success=True, cancelled_friend_requestee=to_friend)


class UnfriendUser(LoginRequiredMixin, NeomodelGraphQLMixin, Output, graphene.Mutation):
    class Arguments:
        friend = graphene.String(required=True)

    unfriended_person = graphene.Field(UserNode)

    @classmethod
    def resolve_mutation(cls, root, info, friend):
        current_user = cls.get_current_user()
        friend = User.nodes.get(uid=friend)
        unfriend_user(actor=current_user, friend=friend)

        return cls(success=True, unfriended_person=friend)


class AcceptFriendRequest(
    LoginRequiredMixin, NeomodelGraphQLMixin, Output, graphene.Mutation
):
    class Arguments:
        requester = graphene.String(required=True)

    friend = graphene.Field(UserNode)

    @classmethod
    def resolve_mutation(cls, root, info, requester):
        current_user = cls.get_current_user()
        requester = User.nodes.get(uid=requester)
        accept_friend_request(actor=current_user, requester=requester)

        return cls(success=True, friend=requester)
