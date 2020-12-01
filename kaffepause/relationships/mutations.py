import graphene
from django.contrib.auth import get_user_model

from kaffepause.common.bases import Mutation, NeomodelGraphQLMixin
from kaffepause.relationships.exceptions import RelationshipAlreadyExists
from kaffepause.relationships.services import (
    accept_friend_request,
    cancel_friend_request,
    send_friend_request,
    unfriend_user,
)
from kaffepause.users.models import User
from kaffepause.users.types import UserNode


class SendFriendRequest(NeomodelGraphQLMixin, Mutation):
    class Arguments:
        to_friend = graphene.String(required=True)

    sent_friend_requestee = graphene.Field(UserNode)

    @classmethod
    def resolve_mutation(cls, root, info, to_friend):
        current_user = cls.get_current_user(info)
        to_friend = User.nodes.get(uid=to_friend)
        try:
            send_friend_request(actor=current_user, to_user=to_friend)
        except RelationshipAlreadyExists as e:
            return cls(errors=e.default_message)

        return cls(success=True, sent_friend_requestee=to_friend)


class CancelFriendRequest(NeomodelGraphQLMixin, Mutation):
    class Arguments:
        to_friend = graphene.String(required=True)

    cancelled_friend_requestee = graphene.Field(UserNode)

    @classmethod
    def resolve_mutation(cls, root, info, to_friend):
        current_user = cls.get_current_user(info)
        to_friend = User.nodes.get(uid=to_friend)
        cancel_friend_request(actor=current_user, to_user=to_friend)

        return cls(success=True, cancelled_friend_requestee=to_friend)


class UnfriendUser(NeomodelGraphQLMixin, Mutation):
    class Arguments:
        friend = graphene.String(required=True)

    unfriended_person = graphene.Field(UserNode)

    @classmethod
    def resolve_mutation(cls, root, info, friend):
        current_user = cls.get_current_user(info)
        friend = User.nodes.get(uid=friend)
        unfriend_user(actor=current_user, friend=friend)

        return cls(success=True, unfriended_person=friend)


class AcceptFriendRequest(NeomodelGraphQLMixin, Mutation):
    class Arguments:
        requester = graphene.String(required=True)

    friend = graphene.Field(UserNode)

    @classmethod
    def resolve_mutation(cls, root, info, requester):
        current_user = cls.get_current_user(info)
        requester = User.nodes.get(uid=requester)
        accept_friend_request(actor=current_user, requester=requester)

        return cls(success=True, friend=requester)


class BlockUser(Mutation):
    class Arguments:
        user = graphene.String(required=True)

    @classmethod
    def resolve_mutation(cls, root, info, user):
        raise NotImplementedError


class UnblockUser(Mutation):
    class Arguments:
        user = graphene.String(required=True)

    @classmethod
    def resolve_mutation(cls, root, info, user):
        raise NotImplementedError
