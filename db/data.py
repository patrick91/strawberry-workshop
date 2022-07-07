from asgiref.sync import sync_to_async
from cursor_pagination import CursorPaginator

from users.models import User

from . import models


class AlreadySubscribedToPodcastError(Exception):
    pass


async def find_podcast_by_id(id: str) -> models.Podcast:
    podcast = models.Podcast.objects.filter(id=id)

    return await sync_to_async(podcast.first)()


async def subscribe_to_podcast(user: User, podcast: models.Podcast) -> None:
    def _subscribe_to_podcast():
        if podcast.subscribers.contains(user):
            raise AlreadySubscribedToPodcastError()

        podcast.subscribers.add(user)

    await sync_to_async(_subscribe_to_podcast)()


async def find_podcasts(
    query: str, first: int = 10, after: str | None = None
) -> tuple[list[models.Podcast], list[str]]:
    def _find():
        podcasts = models.Podcast.objects.filter(title__icontains=query)

        paginator = CursorPaginator(podcasts, ordering=("title", "-id"))
        page = paginator.page(first=first, after=after)

        items = list(page)

        return items, [paginator.cursor(item) for item in items]

    return await sync_to_async(_find)()
