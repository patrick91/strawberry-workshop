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
class Query:
    hello: str

    @strawberry.field
    async def podcast(self, id: strawberry.ID) -> Podcast | None:
        if db_podcast := await data.find_podcast_by_id(id):
            return Podcast.from_db(db_podcast)

        return None


schema = strawberry.Schema(query=Query)
