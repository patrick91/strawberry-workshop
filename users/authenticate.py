from typing import Optional, cast

from asgiref.sync import sync_to_async

from django.contrib.auth import authenticate, login
from django.http import HttpRequest

from .models import User


async def authenticate_and_login(
    request: HttpRequest, *, email: str, password: str
) -> Optional[User]:
    def _authenticate() -> Optional[User]:
        if (user := authenticate(email=email, password=password)) is not None:
            login(request, user)

            return cast(User, user)

        return None

    return await sync_to_async(_authenticate)()
