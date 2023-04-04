from kaffepause.notifications.enums import NotificationEntityType
from django.utils.translation import gettext as _

Messages = {
    NotificationEntityType.USER_FRIEND_ADD: lambda actor_name: _("%(actor_name)s har sendt deg en venneforespørsel.") % {"actor_name": actor_name},
    NotificationEntityType.USER_FRIEND_ACCEPT: lambda actor_name: _("%(actor_name)s godtok venneforespørselen din.") % {"actor_name": actor_name},
    NotificationEntityType.BREAK_INVITATION_SENT: lambda actor_name: _("%(actor_name)s inviterte deg til pause.") % {"actor_name": actor_name},
}
