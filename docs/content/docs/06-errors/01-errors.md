+++
title = "Handling errors"
draft = false
weight = 61
sort_by = "weight"
template = "docs/page.html"
slug = "errors"

[extra]
toc = true
top = false
+++

In this section we'll see how we can handle errors in our GraphQL API. As
mentioned at the beginning any error thrown in the resolvers will be returned to
the client in the `errors` field of the response. For example, trying to fetch
the `hello` field from the following schema:

```python
import strawberry

@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        raise ValueError("An example error")

schema = strawberry.Schema(query=Query)
```

will return a response like this:

```json
{
  "data": {
    "hello": null
  },
  "errors": [
    {
      "message": "An example error",
      "path": ["hello"],
      "locations": [
        {
          "line": 4,
          "column": 9
        }
      ]
    }
  ]
}
```

One issue of errors in GraphQL is that they don't have a type system. This means
that we can't differentiate between different types of errors easily, also they
are harder to use in the client.

Let's see a strategy to make working with errors easier in GraphQL. Let's
improve the previous example, `subscribe_to_podcast` by handling the errors.
This is how the resolver looks right now:

```python
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

There are two cases where we return `False`:

1. The podcast doesn't exist
2. The user is already subscribed to the podcast

Returning `False` is not ideal, because we don't know what happened and we won't
be able to handle the error in the client, for example we can't show a different
message to the user if the podcast doesn't exist or if the user is already

# Expected errors vs unexpected errors

Note how we are talking about expected errors here, the approach described here
works well for expected errors, but it doesn't work for unexpected errors, and
that's fine. Unexpected errors are, well, unexpected, so we shouldn't focus them
as much as we do for expected errors. For example if the database is down, we
shouldn't try to handle that error every resolver. In that case it is fine to
return errors in the GraphQL response and let the client fail in a generic way.

> Note: permission classes always raise an error that will be returned in the
> errors field of the GraphQL response. A user not being logged in is usually an
> unexpected errors, as client would check if the user is logged in before
> allowing them do do any operation.

# Handling errors using union types

Let's see how we can handle errors using union types, this is a great way of
making sure that clients are aware of expected errors and that they can handle
them in a nice way.

As mentioned above we have 3 cases:

1. The podcast doesn't exist
2. The user is already subscribed to the podcast
3. Everything went well

We can use a union type to represent these cases, we'll need to create one type
for each case, and then we can use a union type to represent all of them:

```python
@strawberry.type
class PodcastDoesNotExistError:
    message: str = "Podcast does not exist"

@strawberry.type
class AlreadySubscribedToPodcastError:
    message: str = "Already subscribed to podcast"

@strawberry.type
class SubscribeToPodcastSuccess:
    message: str = "Subscribed to podcast"

SubscribeToPodcastResponse = strawberry.union(
    "SubscribeToPodcastResponse",
    (PodcastDoesNotExistError, AlreadySubscribedToPodcastError, SubscribeToPodcastSuccess),
)
```

then we can update our resolver to return the correct type based on the result
of the operation:

```python
@strawberry.type
class PodcastsMutation:
    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def subscribe_to_podcast(
        self, info: Info[Context, None], id: strawberry.ID
    ) -> SubscribeToPodcastResponse:
        request = info.context["request"]

        db_podcast = await data.find_podcast_by_id(id)

        if not db_podcast:
            return PodcastNotFound()

        user = await request.get_user()

        try:
            await data.subscribe_to_podcast(user, db_podcast)
        except data.AlreadySubscribedToPodcastError:
            return AlreadySubscribedToPodcast()

        return SubscribeToPodcastSuccess(
            podcast=Podcast.from_db(db_podcast),
        )
```

# Dealing with unions on the client

Now that we have a union type, we can use it in the client to handle the errors.
Unions have a special syntax in GraphQL, for our example we can use the
following query to subscribe to a podcast and handle errors:

```graphql
mutation {
  subscribeToPodcast(id: "some id") {
    __typename

    ... on SubscribeToPodcastSuccess {
      podcast {
        id
      }
    }
  }
}
```

This query will return a response like this:

```json
{
  "data": {
    "subscribeToPodcast": {
      "__typename": "SubscribeToPodcastSuccess",
      "podcast": {
        "id": "some id"
      }
    }
  }
}
```

The `__typename` field is used to know which type is being returned, which we
can use on the frontend to show an error message if the type is not
`SubscribeToPodcastSuccess`.

so for example if we try to subscribe to a podcast that doesn't exist, we'll get
a response like this:

```json
{
  "data": {
    "subscribeToPodcast": {
      "__typename": "PodcastDoesNotExistError"
    }
  }
}
```

and we can use the `__typename` field to show the following message to the user:

```
Sorry, the podcast you are trying to subscribe to doesn't exist
```

# Improving the type of the errors using interfaces

You might have noticed that in both errors we have a `message` field and we
could use that on the client to show a message to the user. Currently if we want
to fetch the message for both errors we'd need to run the following query:

```graphql
mutation {
  subscribeToPodcast(id: "some id") {
    __typename

    ... on PodcastDoesNotExistError {
      message
    }

    ... on AlreadySubscribedToPodcastError {
      message
    }
  }
}
```

We can make this better by using interfaces, we can create an interface that
defines the `message` field and then we can make both errors implement that
type:

```python
@strawberry.interface
class Error:
    message: str


@strawberry.type
class PodcastNotFound(Error):
    message: str = "Podcast not found"


@strawberry.type
class AlreadySubscribedToPodcast(Error):
    message: str = "You are already subscribed to this podcast"
```

Then we can update our query to look like this:

```graphql
mutation {
  subscribeToPodcast(id: "some id") {
    __typename

    ... on Error {
      message
    }
  }
}
```

This way we can fetch the message for both errors without having to list all the
errors. And we are still able to fetch additional fields for the error if
needed.
