from typing import List

from kaffepause.notifications.models import Notification


def get_notifications_for(*, actor) -> List[Notification]:
    return actor.notifications.all()
