import logging

import graphene
from django.utils.translation import gettext_lazy as _
from graphene_file_upload.scalars import Upload

from kaffepause.common.bases import LoginRequiredMixin, NeomodelGraphQLMixin, Output
from kaffepause.location.models import Location
from kaffepause.location.services import add_user_location
from kaffepause.location.types import LocationNode
from kaffepause.users.services import change_profile_picture, update_profile, update_preferred_location
from kaffepause.users.types import UserNode

logger = logging.getLogger(__name__)


class AddUserLocation(
    LoginRequiredMixin, Output, graphene.Mutation
):
    class Arguments:
        title = graphene.String(required=True)

    location = graphene.Field(LocationNode)

    @classmethod
    def resolve_mutation(cls, root, info, title):
        user = info.context.user
        location = add_user_location(user=user, title=title)
        logger.debug(f"Successfully added user location (uuid:{location.uuid}, user_uuid:{user.uuid})")
        return cls(success=True, location=location)
