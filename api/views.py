from functools import partial
from typing import Protocol, TypedDict, cast

from asgiref.sync import sync_to_async

from django.contrib.auth.middleware import get_user
from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest, HttpResponse

from strawberry.django.views import AsyncGraphQLView

from users.models import User


# See https://github.com/python/mypy/issues/10750
class _GetUser(Protocol):
    async def __call__(self) -> User | AnonymousUser:
        ...


class HttpRequestWithAsyncGetUser(HttpRequest):
    get_user: _GetUser


class Context(TypedDict):
    request: HttpRequestWithAsyncGetUser
    response: HttpResponse


class PodcastGraphQLView(AsyncGraphQLView):
    async def get_context(
        self, request: HttpRequest, response: HttpResponse
    ) -> Context:
        request.get_user = sync_to_async(partial(get_user, request))  # type: ignore

        return {
            "request": cast(HttpRequestWithAsyncGetUser, request),
            "response": response,
        }
