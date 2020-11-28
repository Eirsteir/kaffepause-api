from kaffepause.users.models import User


def get_user_from_account(user):
    user = User.nodes.get(uid=user.id)
    return user
