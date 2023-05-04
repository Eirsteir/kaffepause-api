import graphene

from kaffepause.common.bases import NeomodelGraphQLMixin
from kaffepause.common.decorators import login_required
from kaffepause.groups.mutations import CreateGroup
from kaffepause.groups.selectors import get_groups_for, get_group
from kaffepause.groups.types import GroupNode


class Query(NeomodelGraphQLMixin, graphene.ObjectType):

    my_groups = graphene.List(GroupNode)
    group = graphene.Field(GroupNode, uuid=graphene.UUID(required=True))

    @classmethod
    @login_required
    def resolve_my_groups(cls, root, info, **kwargs):
        current_user = cls.get_current_user()
        return get_groups_for(user=current_user)

    @classmethod
    @login_required
    def resolve_group(cls, root, info, uuid, **kwargs):
        current_user = cls.get_current_user()
        return get_group(actor=current_user, uuid=uuid)


class Mutation(graphene.ObjectType):
    create_group = CreateGroup.Field()
