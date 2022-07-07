import pytest

from db.models import Podcast


pytestmark = pytest.mark.django_db

SUBSCRIBE_TO_PODCAST_MUTATION = """
    mutation SubscribeToPodcast($id: ID!) {
        subscribeToPodcast(id: $id) {
            __typename
            ... on SubscribeToPodcastSuccess {
                podcast {
                    title
                }
            }
            ... on PodcastNotFound {
                message
            }
            ... on AlreadySubscribedToPodcast {
                message
            }
        }
    }
"""


def test_errors_when_not_logged_in(client):
    response = client.post(
        "/graphql",
        data={
            "query": SUBSCRIBE_TO_PODCAST_MUTATION,
            "variables": {"id": "00000000-0000-0000-0000-000000000000"},
        },
        content_type="application/json",
    )

    data = response.json()

    assert data == {
        "data": None,
        "errors": [
            {
                "locations": [{"column": 9, "line": 3}],
                "message": "User is not authenticated",
                "path": ["subscribeToPodcast"],
            }
        ],
    }


@pytest.fixture
def logged_in_client(client, django_user_model):
    user = django_user_model.objects.create_user(
        email="demo@example.com", password="this is valid", name="Jake"
    )

    client.force_login(user)
    client.user = user
    return client


def test_errors_when_podcast_is_missing(logged_in_client):
    response = logged_in_client.post(
        "/graphql",
        data={
            "query": SUBSCRIBE_TO_PODCAST_MUTATION,
            "variables": {"id": "00000000-0000-0000-0000-000000000000"},
        },
        content_type="application/json",
    )

    data = response.json()

    assert data == {
        "data": {
            "subscribeToPodcast": {
                "__typename": "PodcastNotFound",
                "message": "Podcast not found",
            }
        }
    }


def test_works(logged_in_client):
    podcast = Podcast.objects.create(
        title="Podcast",
        description="A podcast",
    )

    response = logged_in_client.post(
        "/graphql",
        data={
            "query": SUBSCRIBE_TO_PODCAST_MUTATION,
            "variables": {"id": str(podcast.id)},
        },
        content_type="application/json",
    )

    data = response.json()

    assert data == {
        "data": {
            "subscribeToPodcast": {
                "__typename": "SubscribeToPodcastSuccess",
                "podcast": {
                    "title": "Podcast",
                },
            }
        }
    }


def test_fails_if_already_subscribed(logged_in_client):
    podcast = Podcast.objects.create(
        title="Podcast",
        description="A podcast",
    )
    podcast.subscribers.add(logged_in_client.user)

    response = logged_in_client.post(
        "/graphql",
        data={
            "query": SUBSCRIBE_TO_PODCAST_MUTATION,
            "variables": {"id": str(podcast.id)},
        },
        content_type="application/json",
    )

    data = response.json()

    assert data == {
        "data": {
            "subscribeToPodcast": {
                "__typename": "AlreadySubscribedToPodcast",
                "message": "You are already subscribed to this podcast",
            }
        }
    }
