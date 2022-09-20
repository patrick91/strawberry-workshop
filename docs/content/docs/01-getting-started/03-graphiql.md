+++
title = "GraphiQL"
draft = false
weight = 12
sort_by = "weight"
template = "docs/page.html"
setup = "graphiql"

[extra]
toc = true
top = false
+++

Strawberry comes with a built-in GraphiQL interface that you can use to test
your API.

To access it, we need to start the server, by running:

```bash
python manage.py runserver
```

Once you have started the server, you can open GraphiQL at
[http://localhost:8000/graphql](http://localhost:8000/graphql).

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
