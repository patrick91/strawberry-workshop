from asgiref.sync import sync_to_async

from . import models


async def find_podcast_by_id(id: str) -> models.Podcast:
    podcast = models.Podcast.objects.filter(id=id)

    return await sync_to_async(podcast.first)()
