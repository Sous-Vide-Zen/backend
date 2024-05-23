import pytest

from src.base.code_text import (
    CREDENTIALS_WERE_NOT_PROVIDED,
    DONT_HAVE_PERMISSIONS,
)

BASE_URL = "http://127.0.0.1:8000/api/v1"


@pytest.mark.django_db
@pytest.mark.api
class TestUserAPI:
    """
    Class for testing user-related API endpoints.

    Test getting the current user.
    Test getting the current user without authorization.
    Test getting a specific user.
    Test getting a non-existent user.
    Test updating a user.
    Test updating another user (forbidden).
    Test getting a list of users.
    Test getting a list of users without authorization.
    Test deleting another user (forbidden).
    Test deleting a user.
    """

    def test_get_current_user(self, api_client, create_token):
        """
        Test getting the current user.
        Endpoint: http://127.0.0.1:8000/api/v1/auth/users/me/
        """

        access_token = create_token
        api_client.credentials(HTTP_AUTHORIZATION=access_token)
        response = api_client.get(f"{BASE_URL}/auth/users/me/")
        assert response.status_code == 200
        assert "username" in response.json()

    def test_get_current_user_unauthorized(self, api_client):
        """
        Test getting the current user without authorization.
        Endpoint: http://127.0.0.1:8000/api/v1/auth/users/me/
        """

        response = api_client.get(f"{BASE_URL}/auth/users/me/")
        assert response.status_code == 401
        assert response.json() == CREDENTIALS_WERE_NOT_PROVIDED

    def test_get_user(self, api_client, create_token, new_author):
        """
        Test getting a specific user.
        Endpoint: http://127.0.0.1:8000/api/v1/user/{username}/
        """

        username = "user2"
        access_token = create_token
        api_client.credentials(HTTP_AUTHORIZATION=access_token)
        response = api_client.get(f"{BASE_URL}/user/{username}/")
        assert response.status_code == 200

    def test_get_existent_user(self, api_client, create_token):
        """
        Test getting a non-existent user.
        Endpoint: http://127.0.0.1:8000/api/v1/user/{username}/
        """

        username = "nonexistent_user"
        access_token = create_token
        api_client.credentials(HTTP_AUTHORIZATION=access_token)
        response = api_client.get(f"{BASE_URL}/user/{username}/")
        assert response.status_code == 404

    def test_update_user(self, api_client, create_token):
        """
        Test updating a user.
        Endpoint: http://127.0.0.1:8000/api/v1/user/{username}/
        """

        username = "user1"
        access_token = create_token
        api_client.credentials(HTTP_AUTHORIZATION=access_token)
        data = {"display_name": "New Display Name"}
        response = api_client.patch(f"{BASE_URL}/user/{username}/", data=data)
        assert response.status_code == 200

    def test_update_user_forbidden(self, api_client, create_token, new_author):
        """
        Test updating another user (forbidden).
        Endpoint: http://127.0.0.1:8000/api/v1/user/{username}/
        """

        username = "user2"
        access_token = create_token
        api_client.credentials(HTTP_AUTHORIZATION=access_token)
        data = {"display_name": "new Display Name"}
        response = api_client.patch(f"{BASE_URL}/user/{username}/", data=data)
        assert response.status_code == 403
        assert response.data == DONT_HAVE_PERMISSIONS

    def test_update_user_unauthorized(self, api_client, new_user):
        """
        Test updating a user without authorization.
        Endpoint: http://127.0.0.1:8000/api/v1/user/{username}/
        """

        data = {"display_name": "new Display Name"}
        response = api_client.patch(f"{BASE_URL}/user/{new_user.username}/", data=data)
        assert response.status_code == 401
        assert response.data == CREDENTIALS_WERE_NOT_PROVIDED

    def test_get_users(self, api_client, create_token):
        """
        Test getting a list of users.
        Endpoint: http://127.0.0.1:8000/api/v1/users/
        """

        access_token = create_token
        api_client.credentials(HTTP_AUTHORIZATION=access_token)
        response = api_client.get(f"{BASE_URL}/users/")
        assert response.status_code == 200
        assert "count" in response.json()
        assert "results" in response.json()
        assert len(response.json()["results"]) <= 10

    def test_get_users_unauthorized(self, api_client):
        """
        Test getting a list of users without authorization.
        Endpoint: http://127.0.0.1:8000/api/v1/users/
        """

        response = api_client.get(f"{BASE_URL}/users/")
        assert response.status_code == 401
        assert response.data == CREDENTIALS_WERE_NOT_PROVIDED

    def test_delete_other_user(self, api_client, create_token, new_author):
        """
        Test deleting another user (forbidden).
        Endpoint: http://127.0.0.1:8000/api/v1/user/{username}/
        """

        access_token = create_token
        username = "user2"
        api_client.credentials(HTTP_AUTHORIZATION=access_token)
        response = api_client.delete(f"{BASE_URL}/user/{username}/")
        assert response.status_code == 403
        assert response.data == DONT_HAVE_PERMISSIONS

    def test_delete_user(self, api_client, create_token):
        """
        Test deleting a user.
        Endpoint: http://127.0.0.1:8000/api/v1/user/{username}/
        """

        access_token = create_token
        username = "user1"
        api_client.credentials(HTTP_AUTHORIZATION=access_token)
        response = api_client.delete(f"{BASE_URL}/user/{username}/")
        assert response.status_code == 204

    def test_delete_user_unauthorized(self, api_client, new_user):
        """
        Test deleting a user without authorization.
        Endpoint: http://127.0.0.1:8000/api/v1/user/{username}/
        """

        response = api_client.delete(f"{BASE_URL}/user/{new_user.username}/")
        assert response.status_code == 401
        assert response.data == CREDENTIALS_WERE_NOT_PROVIDED


@pytest.mark.django_db
@pytest.mark.api
class TestCreateUser:
    """
    User Create API Test
    http://127.0.0.1:8000/api/v1/auth/users/
    """

    def test_custom_user_create_password_retyped(
        self, api_client, create_token, new_author
    ):
        """
        User Serializers Test
        http://127.0.0.1:8000/api/v1/auth/users/
        """

        email = "p7T6M1@example.com"
        password = "Vasya12345!"
        password2 = "Vasya12345!"

        url = "/api/v1/auth/users/"
        data = {"email": email, "password": password, "password2": password2}

        response = api_client.post(url, data=data)

        assert (
            response.status_code == 201
        ), f"Expected status code 201, but got {response.status_code}"
        assert response.data["username"] == f"user{response.data['id']}"

    def test_custom_user_create_password_non_retyped(
        self, api_client, create_token, new_author
    ):
        """
        User Serializers Test
        http://127.0.0.1:8000/api/v1/auth/users/
        """

        email = "p7T6M1@example.com"
        password = "Vasya12345!"

        url = "/api/v1/auth/users/"
        data = {"email": email, "password": password}

        response = api_client.post(url, data=data)

        assert (
            response.status_code == 400
        ), f"Expected status code 400, but got {response.status_code}"
        assert response.data["password2"][0] == "Обязательное поле."

    def test_custom_user_create_password_retyped_different_password(
        self, api_client, create_token, new_author
    ):
        """
        User Serializers Test
        http://127.0.0.1:8000/api/v1/auth/users/
        """

        email = "p7T6M2@example.com"
        password = "Vasya12345!"
        password2 = "Vasya123456!"

        url = "/api/v1/auth/users/"
        data = {"email": email, "password": password, "password2": password2}

        response = api_client.post(url, data=data)

        assert (
            response.status_code == 400
        ), f"Expected status code 400, but got {response.status_code}"
        assert response.data["password"][0] == "Пароли не совпадают!"
