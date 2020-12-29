import logging

import graphene

from kaffepause.common.bases import LoginRequiredMixin, NeomodelGraphQLMixin, Output
from kaffepause.common.constants import Messages
from kaffepause.users.exceptions import UsernameAlreadyInUse
from kaffepause.users.services import update_profile
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
