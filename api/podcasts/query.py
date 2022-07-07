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

    @strawberry.field
    async def find_podcasts(
        self,
        query: str,
        first: int = 10,
        after: strawberry.ID | None = strawberry.UNSET,
    ) -> list[Podcast]:
        # TODO: enforce max first

        paginated_cursors = await data.find_podcasts(
            query=query,
            first=first,
            after=str(after) if after is not strawberry.UNSET else None,
        )

        # temporary hack
        results = []

        for edge in paginated_cursors.edges:
            podcast = Podcast.from_db(edge.node)
            podcast.id = edge.cursor
            results.append(podcast)

        return results
