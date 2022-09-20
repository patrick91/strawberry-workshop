+++
title = "How GraphQL works"
draft = false
weight = 20
sort_by = "weight"
template = "docs/page.html"

[extra]
toc = true
top = false
+++

In the previous section we learned how a GraphQL type can be created using
Strawberry and we also tried to change what a field returns and tested the
change.

We haven't really discussed what happens when you try do a request in GraphiQL.

## The GraphQL endpoint

One key difference of GraphQL and REST is where you fetch the data from.
Typically in REST APIs you have different endpoints for different resources. In
GraphQL there's only one endpoint, which is usually `/graphql` (but it can be
anything really).

In GraphQL, instead of using URLs, you send a document, specifying the data you
want to fetch.

This is (usually) done by sending a JSON payload to the endpoint, for example
the payload for the query we've been testing so far, will look like this:

```json
{
  "query": "{ hello }"
}
```

## The execution of a GraphQL request

When you send a GraphQL request to the server, the server will parse the
document, validate it and execute it.

### Parsing

The first step is to parse the document, which means that the server will
transform the JSON payload into a GraphQL document.

This GraphQL document will then be used to validate the request and execute it.

### Validation

The next step is to validate the document, which means that the server will
check that the document is valid.

For example it will check that the document is well formed, that the fields
exist and that the types of variables are correct.

### Execution

The last step is to execute the document, which means that the server will
execute the document and return the result.

This is where the resolvers are called and the data is fetched.

## The result of a GraphQL request

When you send a GraphQL request to the server, the server will parse the
document, validate it and execute it.

The result of the execution will be a JSON payload, which will look like this:

```json
{
  "data": {
    "hello": "Hello world"
  }
}
```

The `data` key will contain the data that was requested in the document. If
there are any errors, they will be returned in the `errors` key, for example:

```json
{
  "errors": [
    {
      "message": "Cannot query field \"abc\" on type \"Query\".",
      "locations": [
        {
          "line": 1,
          "column": 3
        }
      ]
    }
  ]
}
```
