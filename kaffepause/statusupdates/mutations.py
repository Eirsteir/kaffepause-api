import graphene

from kaffepause.common.bases import LoginRequiredMixin, NeomodelGraphQLMixin, Output
from kaffepause.statusupdates.enums import StatusUpdateType
from kaffepause.statusupdates.services import update_status
from kaffepause.statusupdates.types import StatusUpdateNode


class UpdateStatus(LoginRequiredMixin, NeomodelGraphQLMixin, Output, graphene.Mutation):
    class Arguments:
        status_type = graphene.Enum.from_enum(StatusUpdateType)(required=True)
        latitude = graphene.Float(required=False)
        longitude = graphene.Float(required=False)

    current_status = graphene.Field(StatusUpdateNode)

    @classmethod
    def resolve_mutation(cls, root, info, status_type, latitude, longitude):
        current_user = cls.get_current_user()
        status_type = StatusUpdateType(status_type)
        current_status = update_status(actor=current_user, status_type=status_type, latitude=latitude, longitude=longitude)
        return cls(success=True, current_status=current_status)
