import strawberry

from .authentication.mutation import AuthenticationMutation
from .podcasts.mutation import PodcastsMutation
from .podcasts.query import PodcastsQuery


@strawberry.type
class Query(PodcastsQuery):
    hello: str


@strawberry.type
class Mutation(AuthenticationMutation, PodcastsMutation):
    hello: str


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
)
