import logging

from kaffepause.notifications.enums import NotificationEntityType
from kaffepause.notifications.messages import Messages
from kaffepause.notifications.models import Notification
from kaffepause.users.models import User

logger = logging.getLogger(__name__)


def notify(*, user: User, entity_type: NotificationEntityType, actor: User) -> None:
    # TODO: fail silently?
    text = Messages[entity_type](user.name)
    notification = Notification(entity_type=entity_type.name, entity_id=user.uuid, text=text).save()
    notification.notifier.connect(user)
    notification.actor.connect(actor)

    logger.debug(f"Notification created (notifier id: {user.uuid}): {notification}")
