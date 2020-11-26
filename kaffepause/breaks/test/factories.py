from factory import SubFactory, post_generation
from factory.django import DjangoModelFactory

from kaffepause.accounts.test.factories import AccountFactory
from kaffepause.breaks.models import Break, BreakInvitation


class BreakFactory(DjangoModelFactory):
    class Meta:
        model = Break

    @post_generation
    def participants(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for participant in extracted:
                self.participants.add(participant)


class BreakInvitationFactory(DjangoModelFactory):
    class Meta:
        model = BreakInvitation

    sender = SubFactory(AccountFactory)
    recipient = SubFactory(AccountFactory)
    subject = SubFactory(BreakFactory)
