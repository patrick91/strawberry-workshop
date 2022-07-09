from datetime import datetime
from uuid import UUID

import strawberry

from api.pagination.types import Connection, Edge, PageInfo
from db import data, models


@strawberry.type
class Podcast:
    id: strawberry.ID
    title: str
    description: str

    @classmethod
    def from_db(cls, db_podcast: models.Podcast) -> "Podcast":
        return cls(
            id=strawberry.ID(db_podcast.id),
            title=db_podcast.title,
            description=db_podcast.description,
        )

    @strawberry.field()
    async def episodes(
        self,
        first: int = 10,
        after: strawberry.ID | None = strawberry.UNSET,
    ) -> Connection["Episode"]:
        # TODO: enforce max first
        paginated_cursors = await data.get_episodes_for_podcast(
            podcast_id=self.id,
            first=first,
            after=str(after) if after is not strawberry.UNSET else None,
        )

        page_info = PageInfo.from_db(paginated_cursors.page_info)

        return Connection(
            page_info=page_info,
            edges=[
                Edge(node=Episode.from_db(edge.node), cursor=edge.cursor)
                for edge in paginated_cursors.edges
            ],
        )


@strawberry.type
class Episode:
    id: strawberry.ID
    title: str
    notes: str
    published_at: datetime

    podcast_id: strawberry.Private[UUID]

    @strawberry.field
    async def podcast(self) -> Podcast:
        from .dataloaders import podcast_loader

        return await podcast_loader.load(str(self.podcast_id))

    @classmethod
    def from_db(cls, db_episode: models.Episode) -> "Episode":
        return cls(
            id=strawberry.ID(db_episode.id),
            title=db_episode.title,
            notes=db_episode.notes,
            published_at=db_episode.published_at,
            podcast_id=db_episode.podcast_id,  # type: ignore
        )
