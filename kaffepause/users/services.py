import logging

from django.core.exceptions import ValidationError

from kaffepause.users.forms import UserUpdateForm
from kaffepause.users.models import User

logger = logging.getLogger(__name__)


def update_profile(*, user: User, **data) -> User:
    logger.debug(f"Updating user (uuid: {user.uuid}")
    print(data)
    form = UserUpdateForm(instance=user, data=data)
    if form.is_valid():
        return form.save()

    logger.info(f"Failed to update user (uuid:{user.uuid})")
    raise ValidationError(form.errors)
