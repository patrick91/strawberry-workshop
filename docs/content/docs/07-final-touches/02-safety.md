+++
title = "Safety"
draft = false
weight = 71
sort_by = "weight"
template = "docs/page.html"
slug = "safety"

[extra]
toc = true
top = false
+++

GraphQL gives clients a lot of flexibility to make queries, but it can also be
dangerous if not used properly.

## Query Depth

GraphQL queries can be nested arbitrarily deep. This can be a problem if an
attacker is able to craft a query that is very deep and causes your server to
work very hard to resolve it.

For example, supposed we implemented a list of episode for a podcast, we could
allow queries like this:

```graphql
{
  podcasts(first: 50) {
    edges {
      node {
        title
        episodes(first: 50) {
          title
        }
      }
    }
  }
}
```

which is fine on its own, but we also allowed clients to fetch the podcast on
the episode node, so we could also run the following query:

```graphql
{
  podcasts(first: 50) {
    edges {
      node {
        title
        episodes(first: 50) {
          podcast {
            episodes(first: 50) {
              podcast {
                episodes(first: 50) {
                  podcast {
                    title
                    # ...
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
```

This query is very deep and could cause our server to work very hard to resolve
it, which could lead to a denial of service attack.

To prevent this, we can limit the depth of the query by using the
`QueryDepthLimiter` extension provided by Strawberry:

```python
schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    extensions=[
        # 8 is the maximum depth in this case
        QueryDepthLimiter(8),
    ],
)
```

## Query Complexity

Another approach to prevent queries that are too complex is to limit the
complexity of the query. This is similar to the query depth, but instead of
limiting the depth of the query, we limit the complexity of the query.

For example, if we have a query like this:

```graphql
{
  podcasts(first: 50) {
    edges {
      node {
        title
        episodes(first: 50) {
          title
        }
      }
    }
  }
}
```

we can assign a complexity to the fields that can be paginated and that
complexity will be equal to the number of items requested, times the complexity
of parent.

For example in this case, the complexity of the `episodes` field would be 50,
and the complexity of the `podcasts` field would be 50 \* 50 = 2500. So the
total complexity of the query would be 2550.

```graphql
{
  # complexity: 50
  podcasts(first: 50) {
    edges {
      node {
        title
        # complexity: 50 * 50 = 2500
        episodes(first: 50) {
          title
        }
      }
    }
  }
}
```

Unfortunately this is not yet built into Strawberry, but it can be implemented
creating an Extension.
