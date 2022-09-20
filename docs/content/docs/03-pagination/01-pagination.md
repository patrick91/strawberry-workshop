+++
title = "Pagination"
draft = false
weight = 31
sort_by = "weight"
template = "docs/page.html"
slug = "pagination"

[extra]
toc = true
top = false
+++

Almost every API needs to paginate data to avoid returning too much data at
once. This is especially true with GraphQL as you can ask for as much data as
you want in a single query.

Let's see how we can create an API that paginates data. We'll be creating a new
field that returns all the podcasts and paginates them.

## Basic pagination

Let's see how we can implement a basic pagination for our API. We'll allow our
users to paginate the podcasts by passing a `page` and `perPage` argument to our
field.

The query will look like this:

```graphql
query {
  podcasts(page: 1, perPage: 10) {
    title
  }
}
```

Our data module exposes a `paginate_podcast` function that we can use to
paginate the podcasts. Let's create a new field on our Query that uses this
function. Go to `podcasts/query.py` and update `PodcastsQuery` to look like
this:

```python
import strawberry


from db import data
from typing import Optional, List
from .types import Podcast


@strawberry.type
class PodcastsQuery:
    # keep the previous fields
    ...

    @strawberry.field
    async def podcasts(self, page: int = 1, per_page: int = 10) -> List[Podcast]:
        db_podcasts = await data.paginate_podcast(page=page, per_page=per_page)

        return [
            Podcast(
                id=db_podcast.id,
                title=db_podcast.title,
                description=db_podcast.description,
            )
            for db_podcast in db_podcasts
        ]
```

Similar to the previous example, we have created a resolver that uses the data
module to fetch the podcasts from the db and returns a list of `Podcast`
objects. One thing to note is that we are using default arguments for `page` and
`per_page`, this means that if the user doesn't pass these arguments, we'll be
using the default values. These defaults are also exposed in GraphQL.

Feel free to go to [GraphiQL](http://localhost:8000/graphql) and try out!

## Some basic validation

We can do some basic validation on the `page` and `per_page` arguments to make
sure that the user is not passing invalid values. Let's update our resolver to
look like this:

```python
import strawberry


from db import data
from typing import Optional, List
from .types import Podcast


@strawberry.type
class PodcastsQuery:
    # keep the previous fields
    ...

    @strawberry.field
    async def podcasts(self, page: int = 1, per_page: int = 10) -> List[Podcast]:
        if page < 1:
            raise ValueError("page must be greater than 0")

        if per_page < 1:
            raise ValueError("per page must be greater than 0")

        if per_page > 50:
            raise ValueError("per page must be less than 50")

        db_podcasts = await data.paginate_podcast(page=page, per_page=per_page)

        return [
            Podcast(
                id=db_podcast.id,
                title=db_podcast.title,
                description=db_podcast.description,
            )
            for db_podcast in db_podcasts
        ]
```

Now if the user passes a `page` or `per_page` that is less than 1 or greater
than 50, we'll raise an error. Every exception that is raised in a resolver will
be returned to the user as an error.

> Note, there are ways of changing how errors are returned to the user, as
> returning all the exceptions might be problematic in some cases.

## Returning has next page

We can also let our clients know if there's more pages in our paginated field.
We can do this by returning a `has_next_page` field in our resolver. We can do
this by creating a new type that contains the `has_next_page` field and the list
of podcasts.

Let's create a new type called `PaginatedPodcasts` that contains the list of
podcasts and the total number of items:

```python
import strawberry
from typing import List

@strawberry.type
class PaginatedPodcasts:
    items: List[Podcast]
    has_next_page: bool
```

We can now update our resolver to return a `PaginatedPodcasts` object:

```python
import strawberry


@strawberry.type
class PodcastsQuery:
    # keep the previous fields
    ...

    @strawberry.field
    async def podcasts(self, page: int = 1, per_page: int = 10) -> PaginatedPodcasts:
        # ... same validation above

        db_podcasts = await data.paginate_podcast(page=page, per_page=per_page)

        return PaginatedPodcasts(
            items=[
                Podcast(
                    id=db_podcast.id,
                    title=db_podcast.title,
                    description=db_podcast.description,
                )
                for db_podcast in db_podcasts
            ],
            has_next_page=db_podcasts.has_next(),
        )
```

We have now updated our resolver to return a `PaginatedPodcasts` object instead
of a list of podcasts. We are also returning a `has_next_page` field that tells
the user if there's more pages.

We can now test this by going to [GraphiQL](http://localhost:8000/graphql) and
running the following query:

```graphql
query {
  podcasts(page: 1, perPage: 1) {
    items {
      title
    }
    hasNextPage
  }
}
```

This pagination works well for small datasets, but might not work super well for
large datasets. Another approach could be to use a cursor based pagination.
We'll also see a specification called Relay that allows us to create a cursor
based pagination and it is quite popular in the GraphQL ecosystem.
