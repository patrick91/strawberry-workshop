import strawberry
from strawberry.extensions import ValidationCache

from .authentication.mutation import AuthenticationMutation
from .podcasts.mutation import PodcastsMutation
from .podcasts.query import PodcastsQuery
from .tracing import DatadogTracingExtension


@strawberry.type
class Query(PodcastsQuery):
    ...


@strawberry.type
class Mutation(AuthenticationMutation, PodcastsMutation):
    ...


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    extensions=[DatadogTracingExtension, ValidationCache()],
)
