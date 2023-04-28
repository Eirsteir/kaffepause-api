import factory
import factory.fuzzy

from kaffepause.breaks.models import Break, BreakInvitation
from kaffepause.common.bases import NeomodelFactory
from kaffepause.common.utils import fifteen_minutes_from_now, time_from_now


class BreakFactory(NeomodelFactory):
    class Meta:
        model = Break

    uuid = factory.Faker("uuid4")
    start_time = factory.fuzzy.FuzzyDateTime(time_from_now(minutes=10), time_from_now(hours=24))


class BreakInvitationFactory(NeomodelFactory):
    class Meta:
        model = BreakInvitation
