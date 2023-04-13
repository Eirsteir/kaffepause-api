import graphene
from graphene import relay
from django.utils.translation import gettext_lazy as _

from kaffepause.breaks.selectors import get_break_history, get_upcoming_breaks
from kaffepause.common.types import CountableConnection
from kaffepause.users.types import UserConnection, UserNode
from kaffepause.location.types import LocationNode


class BreakInvitationNode(graphene.ObjectType):
    class Meta:
        interfaces = (relay.Node,)
        name = "BreakInvitation"

    uuid = graphene.UUID()
    created = graphene.DateTime()
    sender = graphene.Field(UserNode)
    addressee_count = graphene.Int()
    addressees = relay.ConnectionField(UserConnection)
    acceptees = relay.ConnectionField(UserConnection)
    subject = graphene.Field(lambda: BreakNode)

    def resolve_sender(parent, info):
        return parent.get_sender()

    def resolve_addressee_count(parent, info):
        return parent.get_addressee_count()

    def resolve_addressees(parent, info):
        return parent.addressees.all()

    def resolve_acceptees(parent, info):
        return parent.acceptees.all()

    def resolve_subject(parent, info):
        return parent.get_subject()


class BreakNode(graphene.ObjectType):
    class Meta:
        interfaces = (relay.Node,)
        name = "Break"

    uuid = graphene.UUID()
    starting_at = graphene.DateTime()
    participants = relay.ConnectionField(UserConnection)
    invitation = graphene.Field(BreakInvitationNode)
    location = graphene.Field(LocationNode)

    def resolve_invitation(parent, info):
        return parent.get_invitation()

    def resolve_participants(parent, info):
        return parent.get_participants()

    def resolve_location(parent, info):
        return parent.get_location()


class BreakConnection(CountableConnection):
    class Meta:
        node = BreakNode


class BreaksSectionNode(graphene.ObjectType):
    class Meta:
        interfaces = (relay.Node,)
        name = "BreaksSection"

    section_id = graphene.String()
    heading = graphene.String()
    breaks = relay.ConnectionField(BreakConnection)
    is_empty = graphene.Boolean()
    emptyStateText = graphene.String()
    emptyStateActionText = graphene.String()

    def resolve_is_empty(parent, info):
        return not parent.breaks


class BreaksPresentationNode(graphene.ObjectType):
    class Meta:
        interfaces = (relay.Node,)
        name = "BreaksPresentation"

    sections = graphene.List(BreaksSectionNode)

    def resolve_sections(user, info):
        upcoming = BreaksSectionNode(
            section_id="UPCOMING_BREAKS",
            heading=_("Kommende pauser"),
            breaks=get_upcoming_breaks(actor=user),
            emptyStateText=_("Når du er klar for å starte din neste pause, er vi her."),
            emptyStateActionText=_("Planlegg en pause")
        )
        past = BreaksSectionNode(
            section_id="PAST_BREAKS",
            heading=_("Tidligere pauser"),
            breaks=get_break_history(actor=user),
            emptyStateText=_("Kom i gang med pauseplanleggingen"),
            emptyStateActionText=_("Ta din første pause")
        )

        return [upcoming, past]


class BreakInvitationConnection(CountableConnection):
    class Meta:
        node = BreakInvitationNode
