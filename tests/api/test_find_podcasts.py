import string

import pytest

from db.models import Podcast


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
    response = client.post(
        "/graphql",
        data={
            "query": FIND_PODCASTS_QUERY,
            "variables": {"query": "GraphQL"},
        },
        content_type="application/json",
    )

    data = response.json()

    assert data == {"data": {"findPodcasts": {"edges": []}}}


def test_returns_podcasts_when_title_matches(client):
    Podcast.objects.create(title="GraphQL")
    Podcast.objects.create(title="Django")

    response = client.post(
        "/graphql",
        data={
            "query": FIND_PODCASTS_QUERY,
            "variables": {"query": "GraphQL"},
        },
        content_type="application/json",
    )

    data = response.json()
    edges = data["data"]["findPodcasts"]["edges"]

    assert edges[0]["node"]["title"] == "GraphQL"


def test_can_paginate(client):
    for i in range(10):
        Podcast.objects.create(title=f"Podcast {string.ascii_uppercase[i]}")

    response = client.post(
        "/graphql",
        data={
            "query": FIND_PODCASTS_QUERY,
            "variables": {"query": "Podcast", "first": 1},
        },
        content_type="application/json",
    )

    data = response.json()
    edges = data["data"]["findPodcasts"]["edges"]

    assert len(edges) == 1
    assert edges[0]["node"]["title"] == "Podcast A"

    response = client.post(
        "/graphql",
        data={
            "query": FIND_PODCASTS_QUERY,
            "variables": {"query": "Podcast", "first": 1, "after": edges[0]["cursor"]},
        },
        content_type="application/json",
    )

    data = response.json()
    edges = data["data"]["findPodcasts"]["edges"]

    assert len(edges) == 1
    assert edges[0]["node"]["title"] == "Podcast B"