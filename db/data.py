from asgiref.sync import sync_to_async

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
