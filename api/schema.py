import strawberry


@strawberry.type
class Podcast:
    id: strawberry.ID
    title: str
    description: str


@strawberry.type
class Query:
    hello: str

    @strawberry.field
    def podcast(self, id: strawberry.ID) -> Podcast | None:
        return None


schema = strawberry.Schema(query=Query)
