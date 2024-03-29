import graphene
from graphene import relay
from django.utils.translation import gettext_lazy as _

from kaffepause.breaks.enums import InvitationReplyStatus
from kaffepause.breaks.selectors import get_break_history, get_upcoming_breaks, \
    can_user_edit_break, get_pending_break_invitations, get_break_title, get_invitation_context, \
    get_all_break_invitations, get_expired_break_invitations, get_invitation_addressees_annotated
from kaffepause.common.bases import SectionNode
from kaffepause.common.types import CountableConnection
import kaffepause.groups.types
from kaffepause.users.selectors import get_user_from_account
from kaffepause.users.types import UserConnection, UserNode
from kaffepause.location.types import LocationNode


class InvitationAddresseeNode(graphene.ObjectType):
    class Meta:
        interfaces = (relay.Node,)
        name = "InvitationAddressee"

    user = graphene.Field(UserNode)
    rsvp = graphene.String()
    rsvpTitle = graphene.String()


class InvitationAddresseeConnection(CountableConnection):
    class Meta:
        node = InvitationAddresseeNode


class BreakInvitationNode(graphene.ObjectType):
    class Meta:
        interfaces = (relay.Node,)
        name = "BreakInvitation"

    uuid = graphene.UUID()
    created = graphene.DateTime()
    sender = graphene.Field(UserNode)
    addressee_count = graphene.Int()
    addressees = relay.ConnectionField(InvitationAddresseeConnection)
    recipient_group = graphene.Field(lambda: kaffepause.groups.types.GroupNode)
    subject = graphene.Field(lambda: BreakNode)
    context = graphene.Field(graphene.Enum.from_enum(InvitationReplyStatus))

    def resolve_sender(parent, info):
        return parent.get_sender()

    def resolve_addressee_count(parent, info):
        return parent.get_addressee_count()

    def resolve_addressees(parent, info):
        return get_invitation_addressees_annotated(parent)

    def resolve_recipient_group(parent, info):
        return parent.recipient_group.single()

    def resolve_subject(parent, info):
        return parent.get_subject()

    def resolve_context(parent, info):
        current_user_account = info.context.user
        current_user = get_user_from_account(account=current_user_account)
        return get_invitation_context(actor=current_user, invitation=parent)


class BreakNode(graphene.ObjectType):
    class Meta:
        interfaces = (relay.Node,)
        name = "Break"

    uuid = graphene.UUID()
    title = graphene.String()
    starting_at = graphene.DateTime()
    has_passed = graphene.Boolean()
    is_expired = graphene.Boolean()
    participants = relay.ConnectionField(UserConnection)
    initiator = graphene.Field(UserNode)
    invitation = graphene.Field(BreakInvitationNode)
    location = graphene.Field(LocationNode)
    kicker = graphene.String()
    is_viewer_initiator = graphene.Boolean()
    can_viewer_edit_break = graphene.Boolean()
    change_requests = graphene.List(lambda: ChangeRequestNode)

    def resolve_title(parent, info):
        current_user_account = info.context.user
        current_user = get_user_from_account(account=current_user_account)
        return get_break_title(actor=current_user, break_=parent)

    def resolve_invitation(parent, info):
        return parent.get_invitation()

    def resolve_participants(parent, info):
        return parent.get_participants()

    def resolve_location(parent, info):
        return parent.get_location()

    def resolve_is_viewer_initiator(parent, info):
        current_user_account = info.context.user
        current_user = get_user_from_account(account=current_user_account)
        return current_user.is_initiator_of(break_=parent)

    def resolve_can_viewer_edit_break(parent, info):
        current_user_account = info.context.user
        current_user = get_user_from_account(account=current_user_account)
        return can_user_edit_break(user=current_user, break_=parent)

    def resolve_initiator(parent, info):
        return parent.initiator.single()


class BreakConnection(CountableConnection):
    class Meta:
        node = BreakNode


class BreakInvitationConnection(CountableConnection):
    class Meta:
        node = BreakInvitationNode


class BreaksSectionNode(SectionNode, graphene.ObjectType):
    class Meta:
        interfaces = (relay.Node,)
        name = "BreaksSection"

    items = relay.ConnectionField(BreakConnection)


class BreaksPresentationNode(graphene.ObjectType):
    class Meta:
        interfaces = (relay.Node,)
        name = "BreaksPresentation"

    sections = graphene.List(BreaksSectionNode)

    def resolve_sections(user, info):
        upcoming = BreaksSectionNode(
            section_id="UPCOMING_BREAKS",
            heading=_("Kommende pauser"),
            items=get_upcoming_breaks(actor=user),
            emptyStateText=_("Når du er klar for å starte din neste pause, er vi her."),
            emptyStateActionText=_("Planlegg en pause")
        )
        past = BreaksSectionNode(
            section_id="PAST_BREAKS",
            heading=_("Tidligere pauser"),
            items=get_break_history(actor=user),
            emptyStateText=_("Kom i gang med pauseplanleggingen"),
            emptyStateActionText=_("Ta din første pause")
        )

        return [upcoming, past]


class BreakInvitationsSectionNode(SectionNode, graphene.ObjectType):
    class Meta:
        interfaces = (relay.Node,)
        name = "BreakInvitationsSection"

    items = relay.ConnectionField(BreakInvitationConnection)


class BreakInvitationsPresentationNode(graphene.ObjectType):
    class Meta:
        interfaces = (relay.Node,)
        name = "BreakInvitationsPresentation"

    sections = graphene.List(BreakInvitationsSectionNode)

    def resolve_sections(user, info):
        pending = BreakInvitationsSectionNode(
            section_id="PENDING_BREAK_INVITATIONS",
            heading=_("Ventende invitasjoner"),
            items=get_pending_break_invitations(actor=user),
            emptyStateText=_("Kanskje du kan invitere noen på pause?"),
            emptyStateActionText=_("Få med folk på pause")
        )
        expired = BreakInvitationsSectionNode(
            section_id="EXPIRED_BREAK_INVITATIONS",
            heading=_("Utgåtte invitasjoner"),
            items=get_expired_break_invitations(actor=user),
            emptyStateText=_("Ingenting å se her"),
            emptyStateActionText=_("Pause!")
        )
        all = BreakInvitationsSectionNode(
            section_id="ALL_BREAK_INVITATIONS",
            heading=_("Alle invitasjoner"),
            items=get_all_break_invitations(actor=user),
            emptyStateText=_("Ingenting å se her"),
            emptyStateActionText=_("Pause!")
        )

        return [pending, expired, all]


class ChangeRequestNode(graphene.ObjectType):
    class Meta:
        interfaces = (relay.Node,)
        name = "ChangeRequest"

    uuid = graphene.UUID()
    created = graphene.DateTime()
    requested_time = graphene.DateTime()
    requested_location = graphene.Field(LocationNode)
    requested_by = graphene.Field(UserNode)
    requested_for = graphene.Field(BreakNode)
    accepted = graphene.Field(BreakNode)
    denied = graphene.Field(BreakNode)

    def resolve_requested_location(parent, info):
        return parent.requested_location.single()

    def resolve_requested_by(parent, info):
        return parent.requested_by.single()

    def resolve_requested_for(parent, info):
        return parent.requested_for.single()

    def resolve_accepted(parent, info):
        return parent.accepted.single()

    def resolve_denied(parent, info):
        return parent.denied.single()




