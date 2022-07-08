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
class PageInfo:
    has_next_page: bool
    has_previous_page: bool
    start_cursor: str | None
    end_cursor: str | None


@dataclass
class PaginatedData(Generic[T]):
    edges: list[Edge[T]]
    page_info: PageInfo


def paginate(
    queryset: QuerySet[T],
    ordering: Iterable[str],
    first: int = 10,
    after: str | None = None,
) -> PaginatedData[T]:
    paginator = CursorPaginator(queryset, ordering=ordering)
    page = paginator.page(first=first, after=after)
    has_items = len(page) > 0

    page_info = PageInfo(
        has_next_page=page.has_next,
        has_previous_page=page.has_previous,
        start_cursor=paginator.cursor(page[0]) if has_items else None,
        end_cursor=paginator.cursor(page[-1]) if has_items else None,
    )

    return PaginatedData(
        edges=[Edge(node=item, cursor=paginator.cursor(item)) for item in page],
        page_info=page_info,
    )
