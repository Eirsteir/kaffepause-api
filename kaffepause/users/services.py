import logging

from kaffepause.users.exceptions import UsernameAlreadyInUse
from kaffepause.users.models import User

logger = logging.getLogger(__name__)


# TODO: not scalable when new parameters are added
def update_profile(user: User, name: str, username: str) -> User:
    """
    Perform an update on the given user.
    Does not update if the username is already in use
    by another user.
    """
    logger.debug(f"Updating user (uuid: {user.uuid}")

    user_with_username_exists = (
        User.nodes.filter(username__iexact=username)
        .exclude(uuid=user.uuid)
        .get_or_none()
    )

    if user_with_username_exists:
        raise UsernameAlreadyInUse

    user.name = name
    user.username = username
    user.save()
    return user
