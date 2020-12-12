import logging

import graphene
from graphql_jwt.decorators import login_required

from kaffepause.common.bases import NeomodelGraphQLMixin, Output
from kaffepause.common.constants import Messages
from kaffepause.users.exceptions import UsernameAlreadyInUse
from kaffepause.users.models import User
from kaffepause.users.services import update_profile
from kaffepause.users.types import UserNode

logger = logging.getLogger(__name__)


class UpdateProfile(NeomodelGraphQLMixin, Output, graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        username = graphene.String(required=True)

    user = graphene.Field(UserNode)

    @classmethod
    @login_required
    def mutate(cls, root, info, **kwargs):
        account = info.context.user
        user = User.nodes.get(uid=account.id)

        try:
            user = update_profile(user=user, **kwargs)
        except UsernameAlreadyInUse as e:
            logger.info(f"Failed to update user (uid:{user.uid})", exc_info=e)
            return cls(success=False, errors=Messages.USERNAME_IN_USE)

        logger.debug(f"Successfully updated user (uid:{user.uid})")
        return cls(success=True, user=user)
