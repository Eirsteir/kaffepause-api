import graphene

from kaffepause.common.bases import Mutation, NeomodelGraphQLMixin
from kaffepause.statusupdates.enums import StatusUpdateType
from kaffepause.statusupdates.services import update_status
from kaffepause.statusupdates.types import StatusUpdateNode


class UpdateStatus(NeomodelGraphQLMixin, Mutation):
    class Arguments:
        status_type = graphene.Enum.from_enum(StatusUpdateType)(required=True)

    current_status = graphene.Field(StatusUpdateNode)

    @classmethod
    def resolve_mutation(cls, root, info, status_type):
        current_user = cls.get_current_user(info)
        current_status = update_status(actor=current_user, status_type=status_type)
        return cls(success=True, current_status=current_status)
