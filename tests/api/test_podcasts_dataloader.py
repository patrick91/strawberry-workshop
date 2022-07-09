import pytest

from asgiref.sync import sync_to_async

from strawberry.dataloader import DataLoader

from api.podcasts.dataloaders import load_podcasts
from db.models import Podcast


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_dataloader():
    podcast_loader = DataLoader(load_podcasts)

    create = sync_to_async(Podcast.objects.create)

    podcast_1 = await create(title="Podcast 1")
    podcast_2 = await create(title="Podcast 2")
    podcast_3 = await create(title="Podcast 3")

    result = await podcast_loader.load_many(
        [str(podcast_1.id), str(podcast_2.id), str(podcast_3.id)]
    )

    assert result[0].title == "Podcast 1"
    assert result[1].title == "Podcast 2"
    assert result[2].title == "Podcast 3"
