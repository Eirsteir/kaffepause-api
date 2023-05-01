import graphene

from kaffepause.common.bases import LoginRequiredMixin, NeomodelGraphQLMixin, Output
from kaffepause.groups.services import create_group
from kaffepause.groups.types import GroupNode


class CreateGroup(
    LoginRequiredMixin, NeomodelGraphQLMixin, Output, graphene.Mutation
):
    class Arguments:
        name = graphene.String(required=True)

    group = graphene.Field(GroupNode)

    @classmethod
    def resolve_mutation(cls, root, info, name):
        current_user = cls.get_current_user()
        group = create_group(actor=current_user, name=name)
        return cls(group=group, success=True)

