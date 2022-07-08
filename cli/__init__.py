import urllib.request
from datetime import datetime
from typing import cast

import podcastparser
import rich
import typer
from rich.progress import track
from typing_extensions import Required, TypedDict

from django.utils import timezone

from db.models import Episode, Podcast


app = typer.Typer()


class Enclosure(TypedDict):
    url: str
    file_size: int
    mime_type: str


class ParsedEpisode(TypedDict):
    description: str
    published: int
    link: str
    total_time: int
    payment_url: str | None
    enclosures: list[Enclosure]
    title: str
    guid: str
    itunes_author: str
    number: int | None
    explicit: bool
    subtitle: str
    description_html: str


class ItunesOwner(TypedDict):
    name: str
    email: str


class ParsedPodcast(TypedDict, total=False):
    title: Required[str]
    episodes: list[ParsedEpisode]
    description: str
    link: str
    language: str
    itunes_author: str
    itunes_owner: ItunesOwner
    explicit: bool
    cover_url: str
    type: str


@app.command()
def import_feed(feed_url: str):
    current_timezone = timezone.get_current_timezone()

    rich.print(f"Fetching feed from {feed_url}")

    podcast = cast(
        ParsedPodcast, podcastparser.parse(feed_url, urllib.request.urlopen(feed_url))
    )
    episodes = podcast.pop("episodes")

    rich.print(f"Parsed feed: {podcast['title']}")

    db_podcast, _ = Podcast.objects.update_or_create(
        title=podcast["title"],
        defaults={
            "description": podcast.get("description", ""),
            "website": podcast.get("link", ""),
            "image": podcast.get("cover_url", ""),
            "hosted_by": podcast.get("itunes_author", ""),
        },
    )

    rich.print(f"Podcast id: {db_podcast.id}")
    rich.print(f"Found {len(episodes)} episodes")

    for episode in track(episodes, "Importing episodes"):
        published_at = datetime.fromtimestamp(
            episode["published"], tz=current_timezone
        ).isoformat()

        episode, _ = Episode.objects.update_or_create(
            podcast=db_podcast,
            title=episode["title"],
            defaults={
                "notes": episode.get("description", ""),
                "published_at": published_at,
                "total_time": episode.get("total_time", 0),
            },
        )
