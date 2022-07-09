import pytest


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
    ...


def test_errors_when_podcast_is_missing(logged_in_client):
    ...


def test_works(logged_in_client):
    ...


def test_fails_if_already_subscribed(logged_in_client):
    ...
