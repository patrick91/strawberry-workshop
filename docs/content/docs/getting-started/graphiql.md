+++
title = "GraphiQL"
draft = false
weight = 30
sort_by = "weight"
template = "docs/page.html"

[extra]
toc = true
top = false
+++

Once you have started the server, you can open GraphiQL at
http://localhost:8000/graphql.

GraphiQL is a graphical interactive in-browser GraphQL IDE. It is a powerful
tool that allows you to explore your API and test queries.

## Using GraphiQL

To use GraphiQL, you can write your query in the left panel, then click on the
play button to execute it.

Currently our API only has one query, `hello` that returns a string. Try running
the following query:

```graphql
query {
  hello
}
```

You should see the following result:

```json
{
  "data": {
    "hello": "Hello world!"
  }
}
```
