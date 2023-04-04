import graphene
from graphene import relay

from kaffepause.common.bases import NeomodelGraphQLMixin
from kaffepause.common.decorators import login_required
from kaffepause.notifications.selectors import get_notifications_for
from kaffepause.notifications.types import NotificationConnection


class NotificationQuery(NeomodelGraphQLMixin, graphene.ObjectType):

    notifications = relay.ConnectionField(NotificationConnection)

    @classmethod
    @login_required
    def resolve_notifications(cls, root, info, **kwargs):
        # TODO: pagination
        return get_notifications_for(actor=cls.get_current_user())


class Query(NotificationQuery, graphene.ObjectType):
    pass
