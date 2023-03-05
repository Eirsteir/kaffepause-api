import logging
from typing import Iterable
from uuid import UUID

from neomodel import db

from kaffepause.location.enums import LocationRelationship
from kaffepause.location.exceptions import LocationDoesNotExist
from kaffepause.location.models import Location

logger = logging.getLogger(__name__)


def get_location_or_none(*, location_uuid: UUID):
    try:
        return get_location(location_uuid=location_uuid)
    except LocationDoesNotExist as e:
        logger.debug(f"Could not find location with uuid: {location_uuid}. Returning None", exc_info=e)
        return None


def get_location(*, location_uuid: UUID) -> Location:
    try:
        return Location.nodes.get(uuid=location_uuid)
    except Location.DoesNotExist as e:
        logger.debug(f"Could not find location with uuid: {location_uuid}", exc_info=e)
        raise LocationDoesNotExist


def get_locations(*, query: str = None) -> Iterable[Location]:
    """
    Filter locations by given query if present, else return all top leve locations.

    In order to keep the hierarchical location data, only the top level locations
    are returned along with their children.
    """
    if query:
        return Location.nodes.filter(title__icontains=query)

    return _get_top_level_locations()


def _get_top_level_locations():
    query = f"""
    MATCH (location:Location)
    WHERE NOT (location)-[:{LocationRelationship.CHILD_OF}]->(:Location)
    return location
    """
    results, meta = db.cypher_query(query)
    locations = [Location.inflate(row[0]) for row in results]
    return locations
