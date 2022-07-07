import strawberry

from db import data

from .types import Podcast


@strawberry.type
class PodcastsQuery:
    @strawberry.field
    async def podcast(self, id: strawberry.ID) -> Podcast | None:
        if db_podcast := await data.find_podcast_by_id(id):
            return Podcast.from_db(db_podcast)

        return None
