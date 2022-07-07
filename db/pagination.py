from typing import Iterable, TypeVar

from cursor_pagination import CursorPaginator

from django.db.models import Model
from django.db.models.query import QuerySet


T = TypeVar("T", bound=Model, covariant=True)


def paginate(
    queryset: QuerySet[T],
    ordering: Iterable[str],
    first: int = 10,
    after=None,
) -> tuple[list[T], list[str]]:
    paginator = CursorPaginator(queryset, ordering=ordering)
    page = paginator.page(first=first, after=after)

    items = list(page)

    return items, [paginator.cursor(item) for item in items]
