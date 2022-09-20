+++
title = "Duplicated code"
draft = false
weight = 32
sort_by = "weight"
template = "docs/page.html"
slug = "duplicated-code"

[extra]
toc = true
top = false
+++

Before looking at cursor pagination and relay I wanted to address one thing that
I noticed in the previous examples: we have some duplicated code in our
resolvers. We convert the django models into strawberry types in every resolver
by doing:

```python
Podcast(
    id=db_podcast.id,
    title=db_podcast.title,
    description=db_podcast.description,
)
```

I usually move this code on a class method of the type, like this:

```python
import strawberry

from db import data, models


@strawberry.type
class Podcast:
    id: strawberry.ID
    title: str
    description: str

    @classmethod
    def from_db(cls, db_podcast: models.Podcast) -> "Podcast":
        return cls(
            id=strawberry.ID(db_podcast.id),
            title=db_podcast.title,
            description=db_podcast.description,
        )
```

This way we can use it in our resolvers:

```python
@strawberry.type
class PodcastsQuery:
    # keep the previous fields
    ...

    @strawberry.field
    async def podcasts(self, page: int = 1, per_page: int = 10) -> List[Podcast]:
        db_podcasts = await data.paginate_podcast(page=page, per_page=per_page)

        return [Podcast.from_db(db_podcast) for db_podcast in db_podcasts]
```

And we'll avoid having to change the code in multiple places if we need to
change the type.

All our type in future will have this method.
