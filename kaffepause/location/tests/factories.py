import factory


from kaffepause.common.bases import NeomodelFactory
from kaffepause.location.models import Location


class LocationFactory(NeomodelFactory):
    class Meta:
        model = Location

    uuid = factory.Faker("uuid4")
    title = factory.Sequence(lambda n: "Location %03d" % n)

