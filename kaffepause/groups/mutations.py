import graphene

from kaffepause.common.bases import LoginRequiredMixin, NeomodelGraphQLMixin, Output
from kaffepause.groups.services import create_group, remove_group_member
from kaffepause.groups.types import GroupNode
from kaffepause.users.exceptions import UserDoesNotExist


class CreateGroup(
    LoginRequiredMixin, NeomodelGraphQLMixin, Output, graphene.Mutation
):
    class Arguments:
        name = graphene.String(required=True)
        members = graphene.List(graphene.UUID, required=True)

    group = graphene.Field(GroupNode)

    @classmethod
    def resolve_mutation(cls, root, info, name, members):
        current_user = cls.get_current_user()
        group = create_group(actor=current_user, name=name, members=members)
        return cls(group=group, success=True)


class RemoveGroupMember(
    LoginRequiredMixin, NeomodelGraphQLMixin, Output, graphene.Mutation
):
    class Arguments:
        group_uuid = graphene.UUID(required=True)
        member_uuid = graphene.UUID(required=True)

    group = graphene.Field(GroupNode)

    @classmethod
    def resolve_mutation(cls, root, info, group_uuid, member_uuid):
        current_user = cls.get_current_user()
        try:
            group = remove_group_member(actor=current_user, group_uuid=group_uuid, member_uuid=member_uuid)
            return cls(group=group, success=True)
        except UserDoesNotExist as e:
            return cls(group=None, success=False, errors=[e.message])
