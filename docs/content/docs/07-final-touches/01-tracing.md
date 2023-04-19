+++
title = "Tracing"
draft = false
weight = 71
sort_by = "weight"
template = "docs/page.html"
slug = "tracing"

[extra]
toc = true
top = false
+++

Every production API needs to be monitored and traced. Strawberry provides
integration for Datadog and OpenTracing. Tracing is disabled by default, but can
be enabled by adding an extension when creating your schema. In `api/schema.py`
you can add the Datadog tracing extension like this:

```python
from strawberry.extensions.tracing import DatadogTracingExtension

schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    extensions=[
        DatadogTracingExtension,
    ],
)
```

## Strawberry extension

Strawberry has a concept of extensions that can be used to add custom logic to
the execution of a query. Extensions are useful to add tracing, logging, or any
other custom logic.

The Datadog tracing extension hooks into the request start, request end and
resolve functions. It will allow to trace the execution of a query and send the
data to Datadog.

## Example

Getting up and running with datadog or other tracing tools takes a bit of time,
so I'll share a screenshot of what you'll see in the dashboard:

<img src="https://raw.githubusercontent.com/patrick91/strawberry-workshop/main/docs/static/tracing.png" alt="Tracing" width="100%"/>

This view will allow to see the execution time of each field, and the time spend
executing the whole query. You'll also be able to setup filters and metrics on
the dashboard to get more insights on your API.

## Operation names in GraphQL

We haven't talked about operation names yet, but they are an important part of
GraphQL. Operation names are used to identify the query or mutation that is
being executed. They are useful to group queries together, and to identify
queries that are slow using tools like datadog.

For example if we use a query like this:

```graphql
query {
  latestEpisodes {
    title
    podcast {
      title
    }
  }
}
```

we aren't really able to identify the query in datadog, or to distinguish it
from similar queries.

To solve this problem we can add an operation name to the query:

```graphql
query LatestEpisodes {
  latestEpisodes {
    title
    podcast {
      title
    }
  }
}
```

In this case we named our query `LatestEpisodes`, and we can now use this name
to identify the query in datadog.
