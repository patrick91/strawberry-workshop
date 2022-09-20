from typing import List, Optional

from asgiref.sync import sync_to_async

from django.core.paginator import Page, Paginator

from db.pagination import PaginatedData, paginate
from users.models import User

from . import models


class AlreadySubscribedToPodcastError(Exception):
    pass


async def find_podcasts_by_ids(ids: List[str]) -> List[models.Podcast]:
    podcasts = models.Podcast.objects.filter(id__in=ids).all()

    return await sync_to_async(list)(podcasts)


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
    query: Optional[str] = None, first: int = 10, after: Optional[str] = None
) -> PaginatedData[models.Podcast]:
    def _find():
        podcasts = models.Podcast.objects.all()

        if query:
            podcasts = podcasts.filter(title__icontains=query)

        return paginate(
            podcasts,
            ordering=("title", "-id"),
            first=first,
            after=after,
        )

    return await sync_to_async(_find)()


async def find_latest_episodes(last: int = 5) -> List[models.Episode]:
    def _find():
        return models.Episode.objects.order_by("-published_at").all()[:last]

    return await sync_to_async(list)(_find())


async def get_episodes_for_podcast(
    podcast_id: str, first: int = 10, after: Optional[str] = None
) -> PaginatedData[models.Episode]:
    def _find():
        episodes = models.Episode.objects.filter(podcast_id=podcast_id)

        return paginate(
            episodes,
            ordering=("title", "-id"),
            first=first,
            after=after,
        )

    return await sync_to_async(_find)()


async def paginate_podcast(page: int = 1, per_page: int = 10) -> Page[models.Podcast]:
    def _paginate():
        p = Paginator(models.Podcast.objects.all(), per_page)

        paginated_page = p.page(page)

        # TODO: This is a hack to make the paginator work with async
        # we are forcing the paginator to load the data from the database
        # and then we are converting it to a list
        # we do this here because we wrap the this function in sync_to_async
        paginated_page.object_list = list(paginated_page.object_list)

        return paginated_page

    return await sync_to_async(_paginate)()
