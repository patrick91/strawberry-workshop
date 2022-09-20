import strawberry
from strawberry.extensions.query_depth_limiter import QueryDepthLimiter

from .authentication.mutation import AuthenticationMutation
from .podcasts.mutation import PodcastsMutation
from .podcasts.query import PodcastsQuery


@strawberry.type
class Query(PodcastsQuery):
    hello: str = strawberry.field(resolver=lambda: "Hello World! 👋")


@strawberry.type
class Mutation(AuthenticationMutation, PodcastsMutation):
    hello: str


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    extensions=[
        # 8 is the maximum depth in this case
        QueryDepthLimiter(8),
    ],
)
