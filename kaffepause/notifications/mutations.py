import graphene

from kaffepause.breaks.models import BreakInvitation
from kaffepause.breaks.services import (
    accept_break_invitation,
    create_break_and_invitation,
    decline_break_invitation, ignore_break_invitation, request_change,
)
from kaffepause.breaks.types import BreakInvitationNode, BreakNode
from kaffepause.common.bases import LoginRequiredMixin, NeomodelGraphQLMixin, Output
from kaffepause.notifications.services import mark_all_as_seen
from kaffepause.notifications.types import NotificationBadgeCount


class MarkAllAsSeen(
    LoginRequiredMixin, Output, graphene.Mutation
):
    notification_badge_count = graphene.Field(NotificationBadgeCount)

    @classmethod
    def resolve_mutation(cls, root, info):
        current_user = info.context.user
        mark_all_as_seen(user=current_user)
        return cls(notification_badge_count=current_user, success=True)

