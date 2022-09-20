+++
title = "Introspecting operations"
draft = false
weight = 20
sort_by = "weight"
template = "docs/page.html"

[extra]
toc = true
top = false
+++

In the previous section we added a new field to fetch the latest episodes and we
also added the ability of fetching the podcast information for every episode.

In this section we'll see how we could use the information about the GraphQL
request to optimize our data fetching.

## Introspecting the GraphQL request

When running the following GraphQL query:

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

we hit the n+1 problem. We are fetching the latest episodes and then for every
episode we are fetching the podcast information.

We can solve this problem by using the information about the GraphQL request to
fetch the data in a single query.

Strawberry provides information about the GraphQL request in the `info` argument
of the resolver. Let's update our previous resolver to use this information:

```python
from typing import List, Optional

import strawberry
from strawberry.types import Info

from api.pagination.types import Connection, Edge, PageInfo
from api.views import Context
from db import data

from .types import Episode, Podcast


@strawberry.type
class PodcastsQuery:
    # ...

    @strawberry.field
    async def latest_episodes(self, info: Info[Context, None], last: int = 5) -> List[Episode]:
        if last > 50:
            raise ValueError("last must be less than 50")

        current_selected_field = info.selected_fields[0]
        selected_fields = [
            selection.name for selection in current_selected_field.selections
        ]

        if "podcast" in selected_fields:
            # prefetch podcasts
            ...

        episodes = await data.find_latest_episodes(last=last)

        return [Episode.from_db(episode) for episode in episodes]
```

In the previous code we are checking if the `podcast` field is selected in the
GraphQL request. We aren't really doing anything with the information yet, but
you can see how we could pass this information down to `find_latest_episodes`
and use django's prefetching capabilities to optimize the data fetching.

You could also use the information about the request to optimize the query on
the individual field level. The only issue with this approach is that you are
tying your API to the database and you need to make sure to reflect changes in
the database in your API.

Another way to solve this problem is to use a dataloader. We'll see how we can
use dataloaders in the next section.
