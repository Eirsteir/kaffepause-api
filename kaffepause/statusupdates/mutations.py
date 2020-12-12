import graphene
from graphql_jwt.decorators import login_required

from kaffepause.common.bases import NeomodelGraphQLMixin, Output
from kaffepause.statusupdates.enums import StatusUpdateType
from kaffepause.statusupdates.services import update_status
from kaffepause.statusupdates.types import StatusUpdateNode


class UpdateStatus(NeomodelGraphQLMixin, Output, graphene.Mutation):
    class Arguments:
        status_type = graphene.Enum.from_enum(StatusUpdateType)(required=True)

    current_status = graphene.Field(StatusUpdateNode)

    @classmethod
    @login_required
    def mutate(cls, root, info, status_type):
        current_user = cls.get_current_user(info)
        print(status_type.upper())
        status_type = StatusUpdateType[status_type.upper()]
        current_status = update_status(actor=current_user, status_type=status_type)
        return cls(success=True, current_status=current_status)
