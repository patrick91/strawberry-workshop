+++
title = "Strawberry Overview"
draft = false
weight = 22
sort_by = "weight"
template = "docs/page.html"
slug = "strawberry-overview"

[extra]
toc = true
top = false
+++

Let's see how Strawberry works by taking a look at our current API.

```python
import strawberry

from .podcasts.query import PodcastsQuery


@strawberry.type
class Query(PodcastsQuery):
    hello: str = strawberry.field(resolver=lambda: "Hello World!")
```

For the time being we'll be ignoring the imports, they are there to make the
structure of the code manageable.

Let's focus on the the `Query` class. Every GraphQL API needs to have at least
one root type, which is usually called `Query`. This is the entry point for
fetching data in our API.

Let's break the code down, we have a class called `Query`, that has one field
called `hello`, its type is `str` and we are using `strawberry.field` to add
some metadata to this field.

## `strawberry.type`

Finally we have a `@strawberry.type` decorator at the beginning of the class,
this decorator is what transform your python class to a GraphQL type.

`@strawberry.type` does a few things, the most important ones are the following:

1. it uses dataclasses.dataclass to make your class a dataclass
2. it finds all the fields on the class and creates a GraphQL type from it

Using `dataclasses.dataclass` makes your class easier to use, since you'll be
getting useful methods without having to write any code (for example `__init__`,
`__repr__` and `__eq__`)

The creation of the GraphQL type is done by mapping every python type to a
GraphQL type. For example our query class will become the following GraphQL
type:

```graphql
type Query {
  hello: String!
}
```

## Resolvers

When we created the class above we used `strawberry.field` and passed a
"resolver" to our hello field. Resolvers are python functions that are called
when a GraphQL field is requested.

In our example we passed `resolver=lambda: "Hello World!"`, this means that
every time we want to fetch our `hello` field, we'll be calling that lambda
function.

## Try it out!

Feel free to try to change what the lambda function does, you can return a
different text or maybe add the current time to the returned value.
