from dataclasses import dataclass
from typing import Generic, Iterable, TypeVar

from cursor_pagination import CursorPaginator

from django.db.models import Model
from django.db.models.query import QuerySet


T = TypeVar("T", bound=Model, covariant=True)


@dataclass
class Edge(Generic[T]):
    node: T
    cursor: str


@dataclass
class PaginatedData(Generic[T]):
    edges: list[Edge[T]]
    # TODO: add page_info


def paginate(
    queryset: QuerySet[T],
    ordering: Iterable[str],
    first: int = 10,
    after: str | None = None,
) -> PaginatedData[T]:
    paginator = CursorPaginator(queryset, ordering=ordering)
    page = paginator.page(first=first, after=after)

    return PaginatedData(
        edges=[Edge(node=item, cursor=paginator.cursor(item)) for item in page]
    )
