from typing import Iterable

from neomodel import Q

from kaffepause.location.models import Location


def get_locations(*, query: str = None) -> Iterable[Location]:
    # search_query = Q(children=None) | Q(children=[])
    #
    # if query:
    #     search_query = search_query & Q(title__icontains=query)

    return Location.nodes.all()  # filter(search_query)
