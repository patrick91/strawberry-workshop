import strawberry
from strawberry.types import Info

from api.authentication.permissions import IsAuthenticated
from db import data

from .types import Podcast


@strawberry.type
class SubscribeToPodcastSuccess:
    podcast: Podcast


@strawberry.interface
class Error:
    message: str


@strawberry.type
class PodcastNotFound(Error):
    message: str = "Podcast not found"


@strawberry.type
class AlreadySubscribedToPodcast(Error):
    message: str = "You are already subscribed to this podcast"


SubscribeToPodcastResponse = strawberry.union(
    "SubscribeToPodcastResponse",
    (SubscribeToPodcastSuccess, PodcastNotFound, AlreadySubscribedToPodcast),
)


@strawberry.type
class PodcastsMutation:
    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def subscribe_to_podcast(
        self, info: Info, id: strawberry.ID
    ) -> SubscribeToPodcastResponse:
        request = info.context["request"]

        db_podcast = await data.find_podcast_by_id(id)

        if not db_podcast:
            return PodcastNotFound()

        user = await request.get_user()

        try:
            await data.subscribe_to_podcast(user, db_podcast)
        except data.AlreadySubscribedToPodcastError:
            return AlreadySubscribedToPodcast()

        return SubscribeToPodcastSuccess(
            podcast=Podcast.from_db(db_podcast),
        )
