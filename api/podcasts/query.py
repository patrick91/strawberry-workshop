import strawberry

from api.pagination.types import Connection, Edge, PageInfo
from db import data

from .types import Episode, Podcast


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
    ) -> Connection[Podcast]:
        # TODO: enforce max first
        paginated_cursors = await data.find_podcasts(
            query=query,
            first=first,
            after=str(after) if after is not strawberry.UNSET else None,
        )

        page_info = PageInfo.from_db(paginated_cursors.page_info)

        return Connection(
            page_info=page_info,
            edges=[
                Edge(node=Podcast.from_db(edge.node), cursor=edge.cursor)
                for edge in paginated_cursors.edges
            ],
        )

    @strawberry.field
    async def latest_episodes(self, last: int = 5) -> list[Episode]:
        episodes = await data.find_latest_episodes(last=last)

        return [Episode.from_db(episode) for episode in episodes]
