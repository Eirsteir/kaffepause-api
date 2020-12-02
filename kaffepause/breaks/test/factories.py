import factory

from kaffepause.breaks.models import Break, BreakInvitation
from kaffepause.common.bases import NeomodelFactory
from kaffepause.common.utils import fifteen_minutes_from_now


class BreakFactory(NeomodelFactory):
    class Meta:
        model = Break


class BreakInvitationFactory(NeomodelFactory):
    class Meta:
        model = BreakInvitation
