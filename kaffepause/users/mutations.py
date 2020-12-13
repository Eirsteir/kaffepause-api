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

    user = graphene.Field(UserNode)

    @classmethod
    def resolve_mutation(cls, root, info, **kwargs):
        user = cls.get_current_user()
        return cls.__try_to_update_profile(user, **kwargs)

    @classmethod
    def __try_to_update_profile(cls, user, **kwargs):
        try:
            user = update_profile(user=user, **kwargs)
        except UsernameAlreadyInUse as e:
            logger.info(f"Failed to update user (uid:{user.uid})", exc_info=e)
            return cls(success=False, errors=Messages.USERNAME_IN_USE)
        logger.debug(f"Successfully updated user (uid:{user.uid})")
        return cls(success=True, user=user)
