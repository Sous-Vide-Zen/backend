import pytest

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
        assert response.json()["detail"] == "Учетные данные не были предоставлены."

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
        assert (
            response.json()["detail"]
            == "У вас недостаточно прав для выполнения данного действия."
        )

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
        assert response.json()["detail"] == "Учетные данные не были предоставлены."

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
        assert (
            response.json()["detail"]
            == "У вас недостаточно прав для выполнения данного действия."
        )

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
