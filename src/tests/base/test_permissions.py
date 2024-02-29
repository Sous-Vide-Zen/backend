"""
TODO: change test_get_users_by_anonymous url to '/api/v1/users/'
    response.status_code == 401
"""
import pytest


@pytest.mark.django_db
class TestIsOwnerOrAdminOrReadOnly:
    """
    Test is_owner_or_admin_or_readonly permission
    """

    def test_get_users_by_anonymous(self, api_client):
        """
        Test get users by anonymous
        [GET] http://127.0.0.1:8000/api/v1/user/
        """

        response = api_client.get("/api/v1/user/")
        assert response.status_code == 200

    def test_get_user_by_anonymous(self, api_client, new_user):
        """
        Test get user by anonymous
        [GET] http://127.0.0.1:8000/api/v1/user/{username}/
        """

        response = api_client.get(f"/api/v1/user/{new_user.username}/")
        assert response.status_code == 200

    def test_modify_users_by_owner(self, api_client, new_user):
        """
        Test modify users by user
        [PATCH] http://127.0.0.1:8000/api/v1/user/{username}/
        """

        api_client.force_authenticate(user=new_user)
        response = api_client.patch(
            "/api/v1/user/test/", {"first_name": "test"}, format="json"
        )
        assert response.status_code == 200


@pytest.mark.django_db
class TestIsOwnerOrStaffOrReadOnly:
    """
    Test is_owner_or_staff_or_readonly permission
    """

    def test_get_recipe_by_anonymous(self, api_client, new_recipe):
        """
        Test get recipe by anonymous
        [GET] http://127.0.0.1:8000/api/v1/recipe/{slug}/
        """

        response = api_client.get(f"/api/v1/recipe/{new_recipe.slug}/")
        assert response.status_code == 200

    def test_modify_recipe_by_admin(self, api_client, app_admin, new_recipe):
        """
        Test modify recipe by admin
        [PATCH] http://127.0.0.1:8000/api/v1/recipe/{slug}/
        """

        api_client.force_authenticate(user=app_admin)
        response = api_client.patch(
            f"/api/v1/recipe/{new_recipe.slug}/", {"name": "test"}, format="json"
        )
        assert response.status_code == 200
