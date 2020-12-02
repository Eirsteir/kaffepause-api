from kaffepause.breaks.models import Break, BreakInvitation
from kaffepause.common.bases import NeomodelFactory


class BreakFactory(NeomodelFactory):
    class Meta:
        model = Break


class BreakInvitationFactory(NeomodelFactory):
    class Meta:
        model = BreakInvitation
