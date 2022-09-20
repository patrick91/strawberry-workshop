import pytest

from db.models import Episode, Podcast


pytestmark = pytest.mark.django_db

GET_LATEST_EPISODE_QUERY = """
    query GetLatestEpisodes($last: Int!) {
        latestEpisodes(last: $last) {
            title
            podcast {
                title
            }
        }
    }
"""


def test_returns_empty_list_when_there_is_no_episode(client):
    response = client.post(
        "/graphql",
        data={
            "query": GET_LATEST_EPISODE_QUERY,
            "variables": {"last": 5},
        },
        content_type="application/json",
    )

    data = response.json()

    assert data == {"data": {"latestEpisodes": []}}


def test_returns_episodes(client, django_assert_num_queries):
    podcast = Podcast.objects.create(title="GraphQL")
    Episode.objects.create(title="Episode 1", podcast=podcast)
    Episode.objects.create(title="Episode 2", podcast=podcast)

    with django_assert_num_queries(2):
        response = client.post(
            "/graphql",
            data={
                "query": GET_LATEST_EPISODE_QUERY,
                "variables": {"last": 5},
            },
            content_type="application/json",
        )

    data = response.json()

    assert data == {
        "data": {
            "latestEpisodes": [
                {"title": "Episode 2", "podcast": {"title": "GraphQL"}},
                {"title": "Episode 1", "podcast": {"title": "GraphQL"}},
            ]
        }
    }