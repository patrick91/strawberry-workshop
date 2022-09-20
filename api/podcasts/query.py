from typing import List, Optional

import strawberry

from api.pagination.types import Connection, Edge, PageInfo
from db import data

from .types import Episode, Podcast


@strawberry.type
class PodcastsQuery:
    @strawberry.field
    async def podcast(self, id: strawberry.ID) -> Optional[Podcast]:
        db_podcast = await data.find_podcast_by_id(id)

        if db_podcast:
            return Podcast(
                id=db_podcast.id,
                title=db_podcast.title,
                description=db_podcast.description,
            )

        return None

    @strawberry.field
    async def podcasts(
        self,
        first: int = 10,
        after: Optional[strawberry.ID] = None,
    ) -> Connection[Podcast]:
        if first > 50:
            raise ValueError("per page must be less than 50")

        paginated_cursors = await data.find_podcasts(
            first=first,
            after=str(after) if after is not None else None,
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
    async def find_podcasts(
        self,
        query: str,
        first: int = 10,
        after: Optional[strawberry.ID] = None,
    ) -> Connection[Podcast]:
        if first > 50:
            raise ValueError("per page must be less than 50")

        paginated_cursors = await data.find_podcasts(
            query,
            first=first,
            after=str(after) if after is not None else None,
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
    async def latest_episodes(self, last: int = 5) -> List[Episode]:
        episodes = await data.find_latest_episodes(last=last)

        return [Episode.from_db(episode) for episode in episodes]
