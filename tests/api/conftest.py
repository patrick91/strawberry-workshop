import pytest


@pytest.fixture
def logged_in_client(client, django_user_model):
    user = django_user_model.objects.create_user(
        email="demo@example.com", password="this is valid", name="Jake"
    )

    client.force_login(user)
    client.user = user
    return client
