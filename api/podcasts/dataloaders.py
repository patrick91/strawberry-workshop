from strawberry.dataloader import DataLoader

from db import data

from .types import Podcast


async def load_podcasts(ids: list[str]) -> list[Podcast]:
    db_podcasts = await data.find_podcasts_by_ids(ids)

    podcasts_by_id = {
        str(podcast.id): Podcast.from_db(podcast) for podcast in db_podcasts
    }

    return [podcasts_by_id[id] for id in ids]

podcast_loader = DataLoader(load_fn=load_podcasts)
