+++
title = "Authentication"
draft = false
weight = 51
sort_by = "weight"
template = "docs/page.html"
slug = "authentication"

[extra]
toc = true
top = false
+++

In this section we'll see how we can implement authentication for our API.
GraphQL doesn't dictate any way to implement authentication, so we can use any
method we want. It can be a simple API key, a JWT token, a cookie based
authentication or even basic auth.

We'll be using session based authentication in this section. We'll be leveraging
django's authentication so we won't be needing to write much code, fortunately.

## Mutations

This is a good time to talk about mutations. Mutations are the way we can
perform write operations in GraphQL. We can create, update and delete data using
mutations.

We'll be creating a mutation to login users. While login might seem like an
operation that doesn't do any writes, it's actually a write operation. We're
writing a session to the database. And we might also be updating the user with
the last login time.

> Additionally if we enable GraphQL queries via `GET` requests, we don't want
> users to be able to login via a `GET` request.

## Creating the mutation

Mutations in strawberry are very similar to queries. The only difference is we
use `strawberry.mutation` instead of `strawberry.field` when defining the
mutation.

In our project we already have an `api/authentication/mutation.py` file, we can
add our login mutation here.

As usual we also have a function in our data module that will allow us to login
users. We'll be using this function in our mutation.

Let's see how we can implement the login mutation here:

```python
import strawberry
from strawberry.types import Info

from api.views import Context
from users.authenticate import authenticate_and_login


@strawberry.type
class LoginPayload:
    ok: bool


@strawberry.type
class AuthenticationMutation:
    @strawberry.mutation
    async def login(
        self, info: Info[Context, None], email: str, password: str
    ) -> LoginPayload:
        request = info.context["request"]

        user = await authenticate_and_login(request, email=email, password=password)

        if user is not None:
            return LoginPayload(ok=True)

        return LoginPayload(ok=False)
```

This is very similar to what we have done so far with our queries. We have a
`LoginPayload` type that contains a boolean field called `ok`. This field will
be `True` if the login was successful and `False` otherwise.

Our login mutation takes an `email` and a `password` as arguments. But this time
we also have an `info` argument. This argument is a special argument that
contains information about the request. We can use this argument to access the
request object and the user object. In this case `info.context["request"]` will
be the Django HttpRequest object. We'll pass this to `authenticate_and_login` to
login the user.

## Let's test it

Before being able to test this we'll need to create a user, which we can do by
running the following command:

```bash
python manage.py createsuperuser
```

once you have a user you can run the following query to login:

```graphql
mutation {
  login(email: "your@email.com", password: "password") {
    ok
  }
}
```

If you get `ok: true` then you have successfully logged in. The session cookie
will be set in your browser.
