import pytest
from src.apps.follow.models import Follow
from tests.factories.factories import UserFactory


@pytest.mark.django_db
@pytest.mark.api
class TestFollowUrl:
    def test_get_subscriptions_url(self, api_client, new_user):
        url = f"/api/v1/user/{new_user}/subscriptions/"
        api_client.force_authenticate(user=new_user)
        response = api_client.get(url)
        assert response.status_code == 200

    def test_get_followers_url(self, api_client, new_user):
        url = f"/api/v1/user/{new_user}/subscribers/"
        api_client.force_authenticate(user=new_user)
        response = api_client.get(url)
        assert response.status_code == 200

    def test_get_create_subscription_url(self, api_client, new_user):
        url = "/api/v1/subscribe/"
        user = UserFactory.create()
        api_client.force_authenticate(user=new_user)
        response = api_client.post(url, data={"author": user.username}, format="json")
        assert response.status_code == 201

    def test_delete_subscription_url(self, api_client, new_user):
        url = "/api/v1/unsubscribe/"
        user = UserFactory.create()
        api_client.force_authenticate(user=new_user)
        Follow.objects.create(user=new_user, author=user)
        response = api_client.delete(url, data={"author": user.username}, format="json")
        assert response.status_code == 204
