import logging
from uuid import UUID

import cloudinary
import graphene
from django.conf import settings
from graphene_file_upload.scalars import Upload

from kaffepause.common.bases import LoginRequiredMixin, NeomodelGraphQLMixin, Output
from kaffepause.users.services import change_profile_picture, update_profile
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
