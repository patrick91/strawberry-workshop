import pytest


pytestmark = pytest.mark.django_db

FIND_PODCASTS_QUERY = """
    query FindPodcasts($query: String!, $first: Int! = 10, $after: ID) {
        findPodcasts(query: $query, first: $first, after: $after) {
            edges {
                node {
                    title
                }
                cursor
            }
        }
    }
"""


def test_returns_empty_list_when_there_is_no_podcast(client):
    ...


def test_returns_podcasts_when_title_matches(client):
    ...


def test_can_paginate(client):
    ...
