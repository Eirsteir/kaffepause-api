import logging
from typing import Iterable
from uuid import UUID

from neomodel import db, Q

from kaffepause.location.enums import LocationRelationship
from kaffepause.location.exceptions import LocationDoesNotExist
from kaffepause.location.models import Location

logger = logging.getLogger(__name__)


def get_location_or_none(*, location_uuid: UUID):
    return Location.nodes.get_or_none(uuid=location_uuid)


def get_location(*, location_uuid: UUID) -> Location:
    try:
        return Location.nodes.get(uuid=location_uuid)
    except Location.DoesNotExist as e:
        logger.debug(f"Could not find location with uuid: {location_uuid}", exc_info=e)
        raise LocationDoesNotExist


def get_campus_locations(*, query: str = None) -> Iterable[Location]:
    query_filter = Q(item_type="campus")

    if query:
        query_filter &= Q(title__icontains=query)

    return Location.nodes.filter(query_filter)
