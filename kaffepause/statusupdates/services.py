from kaffepause.statusupdates.enums import StatusUpdateType
from kaffepause.statusupdates.models import StatusUpdate
from kaffepause.users.models import User


def update_status(actor: User, status_type: StatusUpdateType, latitude: float = None, longitude: float = None):
    """Update the users current status to that of the given type."""
    new_status = StatusUpdate(
        status_type=status_type.name
    ).save()
    previous_status = actor.current_status.single()

    if previous_status:
        return _change_current_status(actor, previous_status, new_status)

    return _set_new_status(actor, new_status)


def _change_current_status(actor, previous_status, new_status):
    actor.current_status.disconnect(previous_status)
    new_status.previous.connect(previous_status)
    actor.current_status.connect(new_status)
    return new_status


def _set_new_status(actor, new_status):
    actor.current_status.connect(new_status)
    return new_status
