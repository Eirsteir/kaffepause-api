from typing import List
from uuid import UUID

from kaffepause.groups.models import Group
from kaffepause.notifications.enums import NotificationEntityType
from kaffepause.notifications.services import bulk_notify
from kaffepause.users.models import User


def create_group(*, actor: User, name: str, members: List[UUID] = None) -> Group:

    group = Group(name=name).save()
    group.creator.connect(actor)
    group.members.connect(actor)

    if members:
        add_members_to_group(actor, group, members)

    return group


def add_members_to_group(actor, group, members):
    members = actor.friends.filter(uuid__in=members)
    for member in members:
        group.members.connect(member)

    bulk_notify(
        notifiers=members,
        actor=actor,
        entity_type=NotificationEntityType.GROUP_MEMBER_ADDED,
        entity_id=group.uuid,
        group_name=group.name
    )

