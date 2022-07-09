import pytest


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
    ...


def test_finds_podcast(client):
    ...


FIND_PODCAST_WITH_EPISODES_QUERY = """
    query FindPodcastWithEpisodes($id: ID!) {
        podcast(id: $id) {
            id
            title
            episodes(first: 1) {
                edges {
                    node {
                        id
                        title
                    }
                }
            }
        }
    }
"""


def tests_returns_episodes(client):
    ...
