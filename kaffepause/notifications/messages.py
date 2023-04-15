from kaffepause.common.utils import format_time_from_now, format_kicker_message
from kaffepause.notifications.enums import NotificationEntityType
from django.utils.translation import gettext as _


def _get_user_friend_add_message(actor_name, **kwargs):
    return _("%(actor_name)s har sendt deg en venneforespørsel.") % {"actor_name": actor_name, **kwargs}


def _get_user_friend_accept_message(actor_name, **kwargs):
    return _("%(actor_name)s godtok venneforespørselen din.") % {"actor_name": actor_name, **kwargs}


def _get_break_invitation_sent_message(actor_name, **kwargs):
    if kwargs.get("location_name"):
        return _("%(actor_name)s vil ta en pause på %(location_name)s kl %(starting_at)s.") % {"actor_name": actor_name, **kwargs}
    return _("%(actor_name)s vil ta en pause kl %(starting_at)s.") % {"actor_name": actor_name, **kwargs}


def _get_break_invitation_accepted_message(actor_name, **kwargs):
    return _("%(actor_name)s godtok pauseinvitasjonen din.") % {"actor_name": actor_name, **kwargs}


def _get_break_invitation_declined_message(actor_name, **kwargs):
    return _("%(actor_name)s avslo pauseinvitasjonen din.") % {"actor_name": actor_name, **kwargs}


Messages = {
    NotificationEntityType.USER_FRIEND_ADD: _get_user_friend_add_message,
    NotificationEntityType.USER_FRIEND_ACCEPT: _get_user_friend_accept_message,
    NotificationEntityType.BREAK_INVITATION_SENT: _get_break_invitation_sent_message,
    NotificationEntityType.BREAK_INVITATION_ACCEPTED: _get_break_invitation_accepted_message,
    NotificationEntityType.BREAK_INVITATION_DECLINED: _get_break_invitation_declined_message,
}


def _default_no_kicker_message(**kwargs):
    return None


def _get_break_invitation_sent_kicker_message(**kwargs):
    time = kwargs.get("time")
    if time:
        return format_kicker_message(time)
    return None


KickerMessages = {
    NotificationEntityType.USER_FRIEND_ADD: _default_no_kicker_message,
    NotificationEntityType.USER_FRIEND_ACCEPT: _default_no_kicker_message,
    NotificationEntityType.BREAK_INVITATION_SENT: _get_break_invitation_sent_kicker_message,
    NotificationEntityType.BREAK_INVITATION_ACCEPTED: _default_no_kicker_message,
    NotificationEntityType.BREAK_INVITATION_DECLINED: _default_no_kicker_message,
}
