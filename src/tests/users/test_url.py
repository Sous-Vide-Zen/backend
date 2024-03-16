import pytest
from django.core.management import call_command
from rest_framework.test import APIClient

BASE_URL = "http://127.0.0.1:8000/api/v1"


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    """
    Django DB setup.
    """

    with django_db_blocker.unblock():
        call_command("migrate")


@pytest.fixture
def api_client():
    """
    APIClient fixture
    """

    return APIClient()


@pytest.fixture
def create_user1(django_user_model):
    """
    Create a second user with username 'user1'
    """
    user = django_user_model.objects.create_user(
        username="user1", password="password123", email="user1@example.com"
    )

    return user


@pytest.fixture
def create_token(api_client, django_user_model, create_user1):
    """
    Create token
    """

    django_user_model.objects.create_user(
        username="user2", password="changeme123", email="test2@ya.ru"
    )
    response = api_client.post(
        "/api/v1/auth/jwt/create/",
        data={"password": "changeme123", "email": "test2@ya.ru"},
        format="json",
    )
    return response.data["access"]


@pytest.mark.django_db
@pytest.mark.api
class TestUserAPI:
    def test_get_current_user(self, api_client, create_token):
        access_token = create_token
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        response = api_client.get(f"{BASE_URL}/auth/users/me/")
        assert response.status_code == 200
        assert "username" in response.json()

    def test_get_current_user_unauthorized(self, api_client):
        response = api_client.get(f"{BASE_URL}/auth/users/me/")
        assert response.status_code == 401
        assert response.json()["detail"] == "Учетные данные не были предоставлены."

    def test_get_user(self, api_client, create_token):
        username = "user1"
        access_token = create_token
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        response = api_client.get(f"{BASE_URL}/user/{username}/")
        assert response.status_code == 200

    def test_get_existent_user(self, api_client, create_token):
        username = "existent_user"
        access_token = create_token
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        response = api_client.get(f"{BASE_URL}/user/{username}/")
        assert response.status_code == 404

    def test_update_user(self, api_client, create_token):
        username = "user2"
        access_token = create_token
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        data = {"display_name": "New Display Name"}
        response = api_client.patch(f"{BASE_URL}/user/{username}/", data=data)
        assert response.status_code == 200

    def test_update_user_forbidden(self, api_client, create_token):
        username = "user1"
        access_token = create_token
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        data = {"display_name": "new Display Name"}
        response = api_client.patch(f"{BASE_URL}/user/{username}/", data=data)
        assert response.status_code == 403
        assert (
            response.data["detail"]
            == "У вас недостаточно прав для выполнения данного действия."
        )

    def test_get_users(self, api_client, create_token):
        access_token = create_token
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        response = api_client.get(f"{BASE_URL}/users/")
        assert response.status_code == 200
        assert "count" in response.json()
        assert "results" in response.json()
        assert len(response.json()["results"]) <= 10

    def test_get_users_unauthorized(self, api_client):
        response = api_client.get(f"{BASE_URL}/users/")
        assert response.status_code == 401
        assert response.json()["detail"] == "Учетные данные не были предоставлены."

    def test_delete_other_user(self, api_client, create_token):
        access_token = create_token
        username = "user1"
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        response = api_client.delete(f"{BASE_URL}/user/{username}/")
        assert response.status_code == 403
        assert (
            response.json()["detail"]
            == "У вас недостаточно прав для выполнения данного действия."
        )

    def test_delete_user(self, api_client, create_token):
        access_token = create_token
        username = "user2"
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        response = api_client.delete(f"{BASE_URL}/user/{username}/")
        assert response.status_code == 204
