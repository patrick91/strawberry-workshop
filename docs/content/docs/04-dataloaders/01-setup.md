+++
title = "Setup"
draft = false
weight = 41
sort_by = "weight"
template = "docs/page.html"
slug = "setup"

[extra]
toc = true
top = false
+++

In this section we'll see some techniques that we can use to optimize our data
fetching. But before we start we need to add more fields to our API.

Currently we are only able to fetch a list of podcasts and a single podcast.
We'll add a field to fetch the latest episodes (globally) and we'll see how we
can prevent issues like N+1 queries.

## The Episode type

Let's start by adding a new type to our API. We'll be adding a new type called
`Episode` that will represent a single episode.

We'll be adding it to `api/podcasts/types.py` and it will look like this:

```python
from datetime import datetime

import strawberry

from db import models


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


@strawberry.type
class Episode:
    id: strawberry.ID
    title: str
    notes: str
    published_at: datetime
    podcast_id: strawberry.Private[str]

    @strawberry.field
    async def podcast(self) -> Podcast:
        from db import data

        db_podcast = await data.find_podcast_by_id(self.podcast_id)

        assert db_podcast is not None

        return Podcast.from_db(db_podcast)

    @classmethod
    def from_db(cls, db_episode: models.Episode) -> "Episode":
        return cls(
            id=strawberry.ID(db_episode.id),
            title=db_episode.title,
            notes=db_episode.notes,
            published_at=db_episode.published_at,
            podcast_id=db_episode.podcast_id,  # type: ignore
        )
```

There's a couple of things to notice here:

1. we are using the `strawberry.Private` type to mark the `podcast_id` field as
   private. This means that it won't be exposed in the GraphQL schema. We are
   using it because we don't want to expose the `podcast_id` field in the
   GraphQL schema, we want to expose the `podcast` field instead.
2. we are using the `strawberry.field` decorator to define the `podcast` field.
   This is because we need to fetch the podcast from the database, and if we did
   that in the `from_db` method we would be doing a database query for each
   episode, even if the client hasn't requested the podcast field.

## Adding the new query

Now that we have the `Episode` type we can add a new query to fetch the latest
episodes.

We'll be adding it to `api/podcasts/query.py` and it will look like this:

```python

@strawberry.type
class PodcastsQuery:
    # ... keep the other fields

    @strawberry.field
    async def latest_episodes(self, last: int = 5) -> List[Episode]:
        episodes = await data.find_latest_episodes(last=last)

        return [Episode.from_db(episode) for episode in episodes]
```

> Note: we aren't using the relay pagination here to keep things simple for this
> workshop.

## Testing the query

Now that we have the new query we can test it in
[GraphiQL](http://localhost:8000/graphql).

We can run the following query:

```graphql
{
  latestEpisodes {
    title
  }
}
```

and we should get the latest 5 episodes. Let's change the query to also fetch
the podcast and its title:

```graphql
{
  latestEpisodes {
    title
    podcast {
      title
    }
  }
}
```

Nice! We can see that we are able to fetch the data about the podcast in a
single GraphQL query, and when we are not fetching the podcast we are not doing
any (additional) database queries.

Unfortunately when we are fetching the podcast we are doing a database query for
each episode. This is because we are fetching the podcast in the `podcast`
field, and we are doing that for each episode.

In the next section we'll see how we **could** use the information about the
GraphQL operation to optimize the query.
