from typing import Generic, TypeVar

import strawberry


Node = TypeVar("Node")


@strawberry.type
class PageInfo:
    has_next_page: bool
    has_previous_page: bool
    start_cursor: str | None
    end_cursor: str | None


@strawberry.type
class Edge(Generic[Node]):
    node: Node
    cursor: str


@strawberry.type
class Connection(Generic[Node]):
    edges: list[Edge[Node]]
    page_info: PageInfo
