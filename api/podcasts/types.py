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
