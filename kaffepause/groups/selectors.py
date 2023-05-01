from typing import List

from kaffepause.groups.models import Group
from kaffepause.users.models import User


def get_groups_for(user: User) -> List[Group]:
    return user.groups.all()
