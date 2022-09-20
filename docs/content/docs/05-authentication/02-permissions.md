+++
title = "Permissions"
draft = false
weight = 52
sort_by = "weight"
template = "docs/page.html"
slug = "permissions"

[extra]
toc = true
top = false
+++

Strawberry provides a way to define permissions for your fields. This is useful
if you want to restrict access to certain fields based on the user that is
making the request.

## Subscribing to a podcast

Let's see how this work by creating a new mutation that allows the current user
to subscribe to a podcast. In `api/podcasts/mutations.py`, add the following
code:

```python
import strawberry
from strawberry.types import Info

from api.authentication.permissions import IsAuthenticated
from api.views import Context
from db import data


@strawberry.type
class PodcastsMutation:
    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def subscribe_to_podcast(
        self, info: Info[Context, None], id: strawberry.ID
    ) -> SubscribeToPodcastResponse:
        request = info.context["request"]

        db_podcast = await data.find_podcast_by_id(id)

        if not db_podcast:
            return False

        user = await request.get_user()

        try:
            await data.subscribe_to_podcast(user, db_podcast)
        except data.AlreadySubscribedToPodcastError:
            return False

        return True
```

This mutation requires the user to be authenticated, otherwise it will return an
error. If the user is authenticated, we try to subscribe the user to the
podcast. If the user is already subscribed to the podcast (or the podcast
doesn't exist), we return `False`, otherwise we return `True`.

> Note: this API design is not ideal, we'll see how to improve it in the next
> section.

## Permissions classes

The permission we used above is already implemented, but let's see how it work
anyway:

```python
from typing import Any

from strawberry.permission import BasePermission
from strawberry.types import Info

from api.views import Context


class IsAuthenticated(BasePermission):
    message = "User is not authenticated"

    async def has_permission(
        self, source: Any, info: Info[Context, None], **kwargs
    ) -> bool:
        user = await info.context["request"].get_user()

        return user.is_authenticated
```

The API is inspired by Django Rest Framework. There's a method called
`has_permission` that received the `source`, `info` and `kwargs` and returns a
boolean.

Source is parent of the field that is being resolved, info is the info object
and kwargs are the arguments passed to the field.

I personally don't use permission classes for many things, I mostly use them for
making sure the user is authenticated and that's it. You can use them for more
complex things, but it is also worth making sure that the same logic is also
implemented in data layer.
