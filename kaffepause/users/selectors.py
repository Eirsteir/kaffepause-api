from kaffepause.users.models import User


def get_user_from_account(user):
    user = User.nodes.get(uuid=user.id)
    return user
