import pytest

BASE_URL = "http://127.0.0.1:8000/api/v1"


@pytest.mark.django_db
class TestUserSerializer:
    """
    Test User Serializers:
    Test UserListSerializer
    Test CustomUserMeSerializer
    Test CustomUserSerializer
    """

    def test_user_list_serializer(self, api_client, create_token):
        """
        User Serializers Test
        http://127.0.0.1:8000/api/v1/users/
        """

        access_token = create_token
        api_client.credentials(HTTP_AUTHORIZATION=access_token)
        response = api_client.get(f"{BASE_URL}/users/")
        assert response.status_code == 200
        assert "count" in response.json()
        assert "results" in response.data
        results = response.data["results"]
        assert len(results) > 0
        user = results[0]
        assert "id" in user
        assert "username" in user
        assert "display_name" in user
        assert "avatar" in user
        assert "recipes_count" in user
        assert "is_follow" in user
        assert "is_follower" in user
        assert user["username"] == "user1"
        assert user["recipes_count"] == 0
        assert user["is_follow"] is False
        assert user["is_follower"] is False

    def test_custom_user_me_serializer(
        self,
        api_client,
        create_token,
    ):
        """
        User Serializers Test
        http://127.0.0.1:8000/api/v1/auth/users/me/
        """

        access_token = create_token
        api_client.credentials(HTTP_AUTHORIZATION=access_token)
        response = api_client.get(f"{BASE_URL}/auth/users/me/")
        assert response.status_code == 200
        user_data = response.json()
        assert "id" in user_data
        assert "username" in user_data
        assert "display_name" in user_data
        assert "avatar" in user_data
        assert "is_active" in user_data
        assert "is_staff" in user_data
        assert "is_admin" in user_data
        assert user_data["username"] == "user1"
        assert user_data["is_active"] is True
        assert user_data["is_staff"] is False
        assert user_data["is_admin"] is False

    def test_custom_user_serializer(self, api_client, create_token, new_author):
        """
        User Serializers Test
        http://127.0.0.1:8000/api/v1/user/{username}/
        """

        username = "user2"
        access_token = create_token
        api_client.credentials(HTTP_AUTHORIZATION=access_token)
        response = api_client.get(f"{BASE_URL}/user/{username}/")
        assert response.status_code == 200
        user_data = response.json()
        assert "id" in user_data
        assert "username" in user_data
        assert "display_name" in user_data
        assert "email" in user_data
        assert "avatar" in user_data
        assert "phone" in user_data
        assert "date_joined" in user_data
        assert "country" in user_data
        assert "city" in user_data
        assert "first_name" in user_data
        assert "last_name" in user_data
        assert "bio" in user_data
        assert "is_active" in user_data
        assert "is_staff" in user_data
        assert "is_admin" in user_data
        assert user_data["username"] == "user2"
        assert user_data["is_active"] is True
        assert user_data["is_staff"] is False
        assert user_data["is_admin"] is False
