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
