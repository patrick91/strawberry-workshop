import strawberry

from .authentication.mutation import AuthenticationMutation
from .podcasts.mutation import PodcastsMutation
from .podcasts.query import PodcastsQuery


@strawberry.type
class Query(PodcastsQuery):
    ...


@strawberry.type
class Mutation(AuthenticationMutation, PodcastsMutation):
    ...


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
)
