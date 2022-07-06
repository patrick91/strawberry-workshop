from typing import cast

from asgiref.sync import sync_to_async

from django.contrib.auth import authenticate, login
from django.http import HttpRequest

from .models import User


async def authenticate_and_login(
    request: HttpRequest, *, email: str, password: str
) -> User | None:
    def _authenticate() -> User | None:
        if (user := authenticate(email=email, password=password)) is not None:
            login(request, user)

            return cast(User, user)

        return None

    return await sync_to_async(_authenticate)()
