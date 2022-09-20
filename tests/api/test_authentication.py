import pytest

from django.contrib.sessions.models import Session


pytestmark = pytest.mark.django_db

LOGIN_MUTATION = """
    mutation Login($email: String!, $password: String!) {
        login(email: $email, password: $password) {
            ok
        }
    }
"""


def test_fails_when_credentials_are_wrong(client):
    response = client.post(
        "/graphql",
        data={
            "query": LOGIN_MUTATION,
            "variables": {"email": "demo@example.com", "password": "fake"},
        },
        content_type="application/json",
    )

    data = response.json()

    assert data == {"data": {"login": {"ok": False}}}


def test_can_login(client, django_user_model):
    user = django_user_model.objects.create_user(
        email="demo@example.com", password="this is valid", name="Jake"
    )

    response = client.post(
        "/graphql",
        data={
            "query": LOGIN_MUTATION,
            "variables": {"email": "demo@example.com", "password": "this is valid"},
        },
        content_type="application/json",
    )

    data = response.json()

    assert data == {"data": {"login": {"ok": True}}}

    session = Session.objects.get(session_key=response.cookies["sessionid"].value)

    assert session.get_decoded()["_auth_user_id"] == str(user.id)