from typing import Generic, TypeVar

import strawberry

from db.pagination import PageInfo as DBPageInfo


Node = TypeVar("Node")


@strawberry.type
class PageInfo:
    has_next_page: bool
    has_previous_page: bool
    start_cursor: str | None
    end_cursor: str | None

    @classmethod
    def from_db(cls, db_page_info: DBPageInfo) -> "PageInfo":
        return cls(
            has_next_page=db_page_info.has_next_page,
            has_previous_page=db_page_info.has_previous_page,
            start_cursor=db_page_info.start_cursor,
            end_cursor=db_page_info.end_cursor,
        )


@strawberry.type
class Edge(Generic[Node]):
    node: Node
    cursor: str


@strawberry.type
class Connection(Generic[Node]):
    edges: list[Edge[Node]]
    page_info: PageInfo
