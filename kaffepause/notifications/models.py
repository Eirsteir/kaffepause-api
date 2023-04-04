from neomodel import RelationshipTo, StringProperty

from kaffepause.common.models import TimeStampedNode
from kaffepause.common.properties import UUIDProperty
from kaffepause.notifications.enums import SeenState, NotificationRelationship, NotificationEntityType, \
    entityTypeToEndpointMapping
from kaffepause.common.enums import (
    USER,
)
from neomodel import (
    RelationshipFrom,
    RelationshipTo,
    StringProperty,
    One,
)


#  https://docs.djangoproject.com/en/4.0/topics/i18n/translation/#:~:text=The%20strings%20you
class Notification(TimeStampedNode):
    uuid = UUIDProperty()
    seen_state = StringProperty(choices=SeenState.choices(), default=SeenState.UNSEEN.name)
    entity_type = StringProperty(required=True, choices=NotificationEntityType.choices())
    entity_id = StringProperty(required=True)
    text = StringProperty(required=True)
    notifier = RelationshipTo(
        USER, NotificationRelationship.NOTIFIES, cardinality=One
    )
    actor = RelationshipFrom(
        USER, NotificationRelationship.ACTOR, cardinality=One
    )

    @property
    def url(self):
        entity_type = NotificationEntityType[self.entity_type]
        return entityTypeToEndpointMapping[entity_type].single(self.entity_id)
