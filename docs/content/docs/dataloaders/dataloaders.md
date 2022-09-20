+++
title = "Dataloaders"
draft = false
weight = 30
sort_by = "weight"
template = "docs/page.html"

[extra]
toc = true
top = false
+++

In this section we'll see how we can use dataloaders to optimize datafetching
and prevent the N+1 problem.

We'll also see why we have been using async resolvers to fetch data from the
database.

## The N+1 problem

As we've seen in the previous section, the following query will result in a N+1
problem:

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

Now let's see how we can solve this problem using dataloaders.

## Dataloaders

Dataloaders are a technique that allows us to batch multiple data fetching
operations into a single one. They work by collecting all the data fetching
operations that need to be done and then executing them in a single query in the
next event loop tick, which is why we need to be using async for our resolvers.

Let's use dataloaders to optimize the previous query. To do so we need to create
a function to load our data and a dataloader based on that function. Let's start
with the function. Go to `api/podcasts/dataloaders.py` and add the following
function:

```python
from strawberry.dataloader import DataLoader

from db import data

from .types import Podcast


async def load_podcasts(ids: list[str]) -> list[Podcast]:
    db_podcasts = await data.find_podcasts_by_ids(ids)

    podcasts_by_id = {
        str(podcast.id): Podcast.from_db(podcast) for podcast in db_podcasts
    }

    return [podcasts_by_id[id] for id in ids]
```

the API for a dataloader function is pretty simple, it takes a list of ids and
returns a list of objects from those ids.

> Note: the data should be returned in the same order as the ids

Then we can create a dataloader with the following code:

```python
podcast_loader = DataLoader(load_fn=load_podcasts)
```

And that's pretty much it. Let's see how can use this dataloader in our
resolver.

## Using dataloaders

Instead of changing our `latest_episodes` resolver, we'll be working directly
with the `podcast` resolver on the `Episode` type.

Go to `api/podcasts/types.py` and change the `podcast` resolver to the
following:

```python
@strawberry.type
class Episode:
    # ... keep the previous fields

    @strawberry.field
    async def podcast(self) -> Podcast:
        from .dataloaders import podcast_loader

        return await podcast_loader.load(str(self.podcast_id))
```

Now if we run the following query:

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

We'll see that we are only doing a single query to the database, which means
that we are not having the N+1 problem anymore.

## How does it work?

Dataloaders work by collecting all the data fetching operations that need to be
done and then executing them in a single query in the next event loop tick. When
running `dataloader.load` we are adding the data fetching operation to a queue
and the the dataloader will schedule a task to execute all the operations in the
queue in the next event loop.

If you want to learn more about dataloaders, you can read the following article:
https://xuorig.medium.com/the-graphql-dataloader-pattern-visualized-3064a00f319f
