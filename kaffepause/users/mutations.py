import logging

import graphene
from django.utils.translation import gettext_lazy as _
from graphene_file_upload.scalars import Upload

from kaffepause.common.bases import LoginRequiredMixin, NeomodelGraphQLMixin, Output
from kaffepause.location.models import Location
from kaffepause.location.types import LocationNode
from kaffepause.users.services import change_profile_picture, update_profile, update_preferred_location
from kaffepause.users.types import UserNode

logger = logging.getLogger(__name__)


class UpdateProfile(
    LoginRequiredMixin, NeomodelGraphQLMixin, Output, graphene.Mutation
):
    class Arguments:
        name = graphene.String(required=True)
        username = graphene.String(required=True)
        locale = graphene.String(required=True)

    user = graphene.Field(UserNode)

    @classmethod
    def resolve_mutation(cls, root, info, **kwargs):
        user = cls.get_current_user()
        user = update_profile(user=user, **kwargs)
        logger.debug(f"Successfully updated user (uuid:{user.uuid})")
        return cls(success=True, user=user)


class ChangeProfilePicture(
    LoginRequiredMixin, NeomodelGraphQLMixin, Output, graphene.Mutation
):
    class Arguments:
        profile_pic = Upload(required=True)

    user = graphene.Field(UserNode)
    profile_pic = graphene.String()

    @classmethod
    def resolve_mutation(cls, root, info, profile_pic, **kwargs):
        current_user = cls.get_current_user()

        result = change_profile_picture(
            uploaded_by=current_user, profile_picture=profile_pic
        )
        return cls(profile_pic=result.get("secure_url"))


class UpdatePreferredLocation(
    LoginRequiredMixin, NeomodelGraphQLMixin, Output, graphene.Mutation
):
    class Arguments:
        location_uuid = graphene.UUID(required=True)

    user = graphene.Field(UserNode)
    location = graphene.Field(LocationNode)

    @classmethod
    def resolve_mutation(cls, root, info, location_uuid, **kwargs):
        current_user = cls.get_current_user()

        try:
            user = update_preferred_location(
                user=current_user, location_uuid=location_uuid
            )
            logger.debug(f"Successfully updated users preferred location (uuid:{user.uuid}, location_uuid: {location_uuid})")
        except Location.DoesNotExist as e:
            return cls(success=False, errors=[_("Dette stedet eksisterer ikke")])

        return cls(success=True, user=user)
