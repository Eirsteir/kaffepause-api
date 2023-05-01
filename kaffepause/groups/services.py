from kaffepause.groups.models import Group
from kaffepause.users.models import User


def create_group(*, actor: User, name: str) -> Group:
    group = Group(name=name).save()
    group.creator.connect(actor)
    group.members.connect(actor)

    return group

