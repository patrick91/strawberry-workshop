from datetime import datetime

import strawberry

from db import models


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
    podcast_id: strawberry.Private[str]

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