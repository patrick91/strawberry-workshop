import pytest


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
    ...


def test_returns_episodes(client, django_assert_num_queries):
    ...
