import strawberry

from api.pagination.types import Connection, Edge, PageInfo
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
    ) -> Connection[Podcast]:
        # TODO: enforce max first

        paginated_cursors = await data.find_podcasts(
            query=query,
            first=first,
            after=str(after) if after is not strawberry.UNSET else None,
        )

        page_info = PageInfo(
            has_next_page=False,
            has_previous_page=False,
            start_cursor=None,
            end_cursor=None,
        )

        return Connection(
            page_info=page_info,
            edges=[
                Edge(node=Podcast.from_db(edge.node), cursor=edge.cursor)
                for edge in paginated_cursors.edges
            ],
        )
