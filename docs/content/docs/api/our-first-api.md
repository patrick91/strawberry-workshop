+++
title = "Our first API"
draft = false
weight = 30
sort_by = "weight"
template = "docs/page.html"

[extra]
toc = true
top = false
+++

In the previous section we learned the basics of how GraphQL works. In this
section we'll be creating our first GraphQL API.

This API will allow us to fetch a podcast by id, if the podcast doesn't exist
we'll return `None`.

## Datamodel

We already have a database structure in place, this is built using Django
models. The code for all the models lives inside `db/models.py`. Let's take a
look at our model:

```python
class Podcast(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        editable=False,
        null=False,
        unique=True,
        db_index=True,
    )
    title = models.CharField(max_length=500)
    subtitle = models.CharField(max_length=500, blank=True)
    hosted_by = models.CharField(max_length=500)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    image = models.ImageField(upload_to="podcasts/", blank=True)
    # list of links with name and url (spotify, apple music, etc)
    links = models.JSONField(blank=True, default=list)

    subscribers = models.ManyToManyField(
        "users.User", related_name="subscribed_podcasts", blank=True
    )
```

## Creating a GraphQL type

To expose this model in GraphQL we need to create a GraphQL type. We **could**
automatically generate a GraphQL type from the Django model, but we'll be
creating it manually.

> Exposing a model directly from a database is not recommended, as it can lead
> to exposing sensitive data and also it will tie your API to a specific
> database structure.

Let's go in our `api/podcast/types.py` file and create a GraphQL type for our
podcast:

```python
import strawberry


@strawberry.type
class Podcast:
    id: strawberry.ID
    title: str
    description: str
```

Our type is pretty basic at the moment, we're only exposing the `id`, `title`
and `description` fields. We'll be adding more fields later. For now let's allow
our API to fetch a Podcast by ID.

## Creating a GraphQL query

To allow fetching a podcast by id we'll need to a new field to the `Query` type.
Let's go in our `api/podcast/query.py` file and add a new field:

```python
import strawberry

from typing import Optional

from .types import Podcast


@strawberry.type
class PodcastsQuery:
    @strawberry.field
    async def podcast(self, id: strawberry.ID) -> Optional[Podcast]:
        return None
```

`PodcastsQuery` is extend in the main `Query` type, so we can keep all the
queries related to podcasts in a single place.

Let's break the code down, we have a class called `PodcastsQuery`, that has one
field called `podcast`, its type is `Optional[Podcast]` and we are using
`strawberry.field` as a _decorator_ to add the resolver directly to the field.

> You can also pass the resolver as an argument to the `strawberry.field` as we
> did in our `hello` field in the previous section.

One thing to note here is that we have an argument called `id` on our resolver,
this argument is automatically converted to a GraphQL argument. This means that
we can now query our API like this:

```graphql
query {
  podcast(id: "some-id") {
    id
    title
    description
  }
}
```

## Return a real podcast

We are now ready to return a real podcast from our API. Let's go in our
`api/podcast/query.py` file and update the `podcast` resolver:

```python
import strawberry


from db import data

from .types import Episode, Podcast


@strawberry.type
class PodcastsQuery:
    @strawberry.field
    async def podcast(self, id: strawberry.ID) -> Podcast | None:
        db_podcast = await data.find_podcast_by_id(id):

        if db_podcast:
            return Podcast(
                id=db_podcast.id,
                title=db_podcast.title,
                description=db_podcast.description,
            )

        return None
```

We are now using the `data` module to fetch the podcast from the database. If
the podcast exists we return a `Podcast` object, otherwise we return `None`.

The `data` module exposes an async API to fetch data from the database, we'll
see why this is important when we discuss dataloaders.

## Testing the API

Let's test that our API returns the right data. But first, we need to fetch an
id for a valid podcast in our database. We can do this by running the following
command:

```bash
python cli.py get-podcasts-ids
```

This command returns a list of ids for first 5 the podcasts in our database.
Let's use one of these ids to test our API.

We can now run the following query:

```graphql
query {
  podcast(id: "the-id") {
    id
    title
    description
  }
}
```

If everything went well you should see something like this:

```json
{
  "data": {
    "podcast": {
      "id": "the-id",
      "title": "The title",
      "description": "The description"
    }
  }
}
```
