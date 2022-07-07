from typing import Any

from strawberry.permission import BasePermission
from strawberry.types import Info


class IsAuthenticated(BasePermission):
    message = "User is not authenticated"

    async def has_permission(self, source: Any, info: Info, **kwargs) -> bool:
        user = await info.context["request"].get_user()

        return user.is_authenticated
