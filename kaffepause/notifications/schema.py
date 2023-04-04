import graphene
from graphene import relay

from kaffepause.common.bases import NeomodelGraphQLMixin
from kaffepause.common.decorators import login_required
from kaffepause.notifications.selectors import get_notifications_for, get_notification_badge_count
from kaffepause.notifications.types import NotificationConnection, NotificationBadgeCount


class NotificationQuery(NeomodelGraphQLMixin, graphene.ObjectType):

    notifications = relay.ConnectionField(NotificationConnection)
    notification_badge_count = graphene.Field(NotificationBadgeCount)

    @classmethod
    @login_required
    def resolve_notifications(cls, root, info, **kwargs):
        # TODO: pagination
        return get_notifications_for(actor=cls.get_current_user())

    @classmethod
    @login_required
    def resolve_notification_badge_count(cls, root, info, **kwargs):
        return cls.get_current_user()


class Query(NotificationQuery, graphene.ObjectType):
    pass
