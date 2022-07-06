import pytest

from db.models import Podcast


pytestmark = pytest.mark.django_db

FIND_PODCAST_BY_ID_QUERY = """
    query FindPodcastById($id: ID!) {
        podcast(id: $id) {
            id
            title
        }
    }
"""


def test_returns_none_when_there_is_no_podcast(client):
    response = client.post(
        "/graphql",
        data={
            "query": FIND_PODCAST_BY_ID_QUERY,
            "variables": {"id": "00000000-0000-0000-0000-000000000000"},
        },
        content_type="application/json",
    )

    data = response.json()

    assert data == {"data": {"podcast": None}}


def test_finds_podcast(client):
    podcast = Podcast.objects.create(title="Podcast 1", description="This is a podcast")

    response = client.post(
        "/graphql",
        data={
            "query": FIND_PODCAST_BY_ID_QUERY,
            "variables": {"id": str(podcast.id)},
        },
        content_type="application/json",
    )

    data = response.json()

    assert data == {
        "data": {
            "podcast": {
                "id": str(podcast.id),
                "title": "Podcast 1",
            }
        }
    }
