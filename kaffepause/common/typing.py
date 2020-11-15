from typing import Generic, List, TypeVar, Union

from django.db.models import QuerySet as DjangoQuerySet

T = TypeVar("T")
QuerySet = Union[DjangoQuerySet, List[T]]
