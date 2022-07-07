from datetime import datetime
from uuid import UUID

import strawberry

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


@strawberry.type
class Episode:
    id: strawberry.ID
    title: str
    notes: str
    published_at: datetime

    podcast_id: strawberry.Private[UUID]

    @strawberry.field
    async def podcast(self) -> Podcast:
        db_podcast = await data.find_podcast_by_id(str(self.podcast_id))

        return Podcast.from_db(db_podcast)

    @classmethod
    def from_db(cls, db_episode: models.Episode) -> "Episode":
        return cls(
            id=strawberry.ID(db_episode.id),
            title=db_episode.title,
            notes=db_episode.notes,
            published_at=db_episode.published_at,
            podcast_id=db_episode.podcast_id,  # type: ignore
        )
