from typing import List, TypeVar, Union

from django.db.models import QuerySet as DjangoQuerySet

T = TypeVar("T")


class QuerySet(Union[DjangoQuerySet, List[T]]):
    pass
