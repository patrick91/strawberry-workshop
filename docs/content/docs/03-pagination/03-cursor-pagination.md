+++
title = "Cursor pagination"
draft = false
weight = 33
sort_by = "weight"
template = "docs/page.html"
slug = "cursor-pagination"

[extra]
toc = true
top = false
+++

As mentioned in the previous section we can use cursor pagination when we have a
lot of data as using an offset based pagination might not be performant.

In this section we'll see how we can implement a cursor based pagination for our
API. We'll allow our users to paginate the podcasts by passing a `cursor` and
we'll be using the
[relay specification](https://relay.dev/graphql/connections.htm) to do so.

## Relay specification

The relay specification defines how we can implement a cursor based pagination
for our API. It defines a `Connection` type that contains a list of nodes and
some metadata about the pagination.

The `Connection` type also defines a `PageInfo` type that contains information
about the current page and if there are more pages.

The `PageInfo` type contains the following fields: `hasNextPage`,
`hasPreviousPage`, `startCursor` and `endCursor`.

The `startCursor` and `endCursor` fields are the cursors for the first and last
node in the list of nodes.

## An example query

```graphql
{
  podcasts(first: 2) {
    pageInfo {
      hasNextPage
    }
    edges {
      cursor
      node {
        title
      }
    }
  }
}
```

This query is more verbose than the previous one, but it provides us with more
information about the pagination.

## Implementing the cursor pagination

As with all our previous examples we also have function inside the data module
that will allow us to paginate data using cursors. The function is called
`find_podcasts` and allows to pass a `first` and `after` argument.

> Note: we are not implementing `before` and `last` but they can be implemented
> in a similar way.

Under the hood `find_podcasts` uses `django-cursor-pagination` to paginate the
data using performant cursors.

Before being able to implement the resolver, we need to implement the types for
our pagination. The types we need to create are the following:

- `PodcastConnection` which is what will be returned by the `podcasts` field.
- `PageInfo` which is the type for the `pageInfo` field.
- `PodcastEdge` which is the type for the `edges` field.

## Using python's generic types

Implementing these types all by hand can be tedious and error prone. Luckily
python has a feature called
[generic types](https://docs.python.org/3/library/typing.html#generics) that
allows us to create types that can be reused.

Strawberry is able to use Python's generic types to create types for us. Our
project has these generic types already implemented for us, so we can use them
to create our types.

They are defined inside `api/pagination/types.py` and look like this:

```python
from typing import Generic, TypeVar, Optional

import strawberry

from db.pagination import PageInfo as DBPageInfo


Node = TypeVar("Node")


@strawberry.type
class PageInfo:
    has_next_page: bool
    has_previous_page: bool
    start_cursor: Optional[str]
    end_cursor: Optional[str]


@strawberry.type
class Edge(Generic[Node]):
    node: Node
    cursor: str


@strawberry.type
class Connection(Generic[Node]):
    edges: list[Edge[Node]]
    page_info: PageInfo
```

We have defined the 3 types we need to implement our pagination, two of them use
python's generic types, `Edge` and `Connection`. We can use these types to
create our types for the pagination.

## Using the generic types

We can use the generic types to create our types for the pagination. We can
immediately use them when defining our field and resolver for the `podcasts`
field.

```python
import strawberry
from typing import Optional

from api.pagination.types import Connection, Edge, PageInfo
from db import data

from .types import Podcast


@strawberry.type
class PodcastsQuery:
    # ... keep the other fields
    @strawberry.field
    async def podcasts(
        self,
        first: int = 10,
        after: Optional[strawberry.ID] = None,
    ) -> Connection[Podcast]:
        if first > 50:
            raise ValueError("per page must be less than 50")

        paginated_cursors = await data.find_podcasts(
            first=first,
            after=str(after) if after is not None else None,
        )

        page_info = PageInfo.from_db(paginated_cursors.page_info)

        return Connection(
            page_info=page_info,
            edges=[
                Edge(node=Podcast.from_db(edge.node), cursor=edge.cursor)
                for edge in paginated_cursors.edges
            ],
        )
```

We can see that we are using the `Connection` type to define the return type of
our field by doing `Connection[Podcast]`. Strawberry is able to use the generic
type to create the type for us, it will automatically create a type called
`PodcastConnection` that will be added to our schema. This is done recursively
for all types that use the TypeVar, so we'll also have a `PodcastEdge` type
defined for us.

If you want to learn more about pagination feel free to read this article:
https://www.apollographql.com/blog/graphql/pagination/understanding-pagination-rest-graphql-and-relay/
