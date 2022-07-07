from functools import partial
from typing import Any

from asgiref.sync import sync_to_async

from django.contrib.auth.middleware import get_user
from django.http import HttpRequest, HttpResponse

from strawberry.django.views import AsyncGraphQLView


class PodcastGraphQLView(AsyncGraphQLView):
    async def get_context(self, request: HttpRequest, response: HttpResponse) -> Any:
        request.get_user = sync_to_async(partial(get_user, request))  # type: ignore

        return {"request": request, "response": response, "get_user": get_user}
