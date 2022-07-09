import pytest


pytestmark = pytest.mark.django_db

LOGIN_MUTATION = """
    mutation Login($email: String!, $password: String!) {
        login(email: $email, password: $password) {
            ok
        }
    }
"""


def test_fails_when_credentials_are_wrong(client):
    ...


def test_can_login(client, django_user_model):
    ...
