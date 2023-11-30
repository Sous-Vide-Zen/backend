import pytest
from django.core.management import call_command
from rest_framework.test import APIClient


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command("migrate")


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_token(api_client, django_user_model):
    django_user_model.objects.create_user(
        username="test", password="changeme123", email="test@ya.ru"
    )
    response = api_client.post(
        "/auth/jwt/create/",
        data={"password": "changeme123", "email": "test@ya.ru"},
        format="json",
    )
    print(f'Bearer {response.data["access"]}')
    return f'Bearer {response.data["access"]}'
