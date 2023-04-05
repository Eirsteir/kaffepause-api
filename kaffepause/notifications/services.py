import logging
from typing import List
from uuid import UUID

from kaffepause.notifications.enums import NotificationEntityType
from kaffepause.notifications.messages import Messages
from kaffepause.notifications.models import Notification
from kaffepause.users.models import User

logger = logging.getLogger(__name__)


# TODO: signals: https://github.com/neo4j-contrib/django-neomodel#signals
def bulk_notify(*, notifiers: List[User], entity_type: NotificationEntityType, entity_id: UUID, actor: User) -> None:
    for notifier in notifiers:
        notify(user=notifier, entity_type=entity_type, entity_id=entity_id, actor=actor)


def notify(*, user: User, entity_type: NotificationEntityType, entity_id: UUID, actor: User) -> None:
    # TODO: fail silently?
    text = Messages[entity_type](actor.name)
    notification = Notification(entity_type=entity_type.name, entity_id=entity_id, text=text).save()
    notification.notifier.connect(user)
    notification.actor.connect(actor)

    logger.debug(f"Notification created (notifier id: {user.uuid}): {notification}")
