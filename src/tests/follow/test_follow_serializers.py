import factory
import pytest
from factory.django import DjangoModelFactory

from src.apps.follow.models import Follow
from src.apps.users.models import CustomUser


class CustomUserFactory(DjangoModelFactory):
    class Meta:
        model = CustomUser

    username = factory.Sequence(lambda n: f"test_user_{n}")
    email = factory.LazyAttribute(lambda o: f"{o.username}@x.com")
    password = "test_password"


@pytest.mark.django_db
@pytest.mark.api
class TestFollowSerializers:
    def test_follow_list_serializer(self, api_client, new_user, new_author):
        """
        Follow serializers test
        """
        Follow.objects.create(user=new_user, author=new_author)
        url = f"/api/v1/user/{new_user}/subscriptions/"
        api_client.force_authenticate(user=new_user)
        response = api_client.get(url)
        assert response.status_code == 200
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["author"]["username"] == new_author.username
        assert response.data["results"][0]["author"]["id"] == new_author.id
        assert response.data["results"][0]["author"]["avatar"] == new_author.avatar
        assert response.data["results"][0]["author"]["bio"] == new_author.bio
        assert response.data["results"][0]["subscribers_count"] == 1

    def test_follower_list_serializer(self, api_client, new_user, new_author):
        """
        Follower serializers test
        """
        Follow.objects.create(user=new_user, author=new_author)
        url = f"/api/v1/user/{new_author}/subscribers/"
        api_client.force_authenticate(user=new_user)
        response = api_client.get(url)
        assert response.status_code == 200
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["user"]["username"] == new_user.username
        assert response.data["results"][0]["user"]["id"] == new_user.id
        assert response.data["results"][0]["user"]["avatar"] == new_user.avatar
        assert response.data["results"][0]["user"]["bio"] == new_user.bio
        assert response.data["results"][0]["subscribers_count"] == 0

    def test_follow_create_serializer(self, api_client, new_user, new_author):
        """
        Follow serializers test
        """
        url = "/api/v1/subscribe/"
        api_client.force_authenticate(user=new_user)
        response = api_client.post(
            url, data={"author": new_author.username}, format="json"
        )
        assert response.status_code == 201
        assert Follow.objects.filter(user=new_user, author=new_author).exists()

    def test_follow_create_non_authenticated(self, api_client, new_user, new_author):
        """
        Follow serializers test non authenticated
        """
        url = "/api/v1/subscribe/"
        response = api_client.post(
            url, data={"author": new_author.username}, format="json"
        )
        assert response.status_code == 401
        assert response.data == {
            "detail": "Authentication credentials were not provided."
        }

    def test_follow_create_already_followed(self, api_client, new_user, new_author):
        """
        Follow serializers test already followed
        """
        Follow.objects.create(user=new_user, author=new_author)
        url = "/api/v1/subscribe/"
        api_client.force_authenticate(user=new_user)
        response = api_client.post(
            url, data={"author": new_author.username}, format="json"
        )
        assert response.status_code == 400

    def test_follow_create_not_found(self, api_client, new_user, new_author):
        """
        Follow serializers test not found
        """
        url = "/api/v1/subscribe/"
        api_client.force_authenticate(user=new_user)
        response = api_client.post(url, data={"author": "Python"}, format="json")
        assert response.status_code == 404
        assert response.data == {"message": "Автор не найден"}

    def test_follow_delete_serializer(self, api_client, new_user, new_author):
        """
        Follow serializers test
        """
        Follow.objects.create(user=new_user, author=new_author)
        url = "/api/v1/unsubscribe/"
        api_client.force_authenticate(user=new_user)
        response = api_client.delete(
            url, data={"author": new_author.username}, format="json"
        )
        assert response.status_code == 204
        assert not Follow.objects.filter(user=new_user, author=new_author).exists()

    def test_follow_delete_non_authenticated(self, api_client, new_user, new_author):
        """
        Follow serializers test non authenticated
        """
        Follow.objects.create(user=new_user, author=new_author)
        url = "/api/v1/unsubscribe/"
        response = api_client.delete(
            url, data={"author": new_author.username}, format="json"
        )
        assert response.status_code == 401
        assert response.data == {
            "detail": "Authentication credentials were not provided."
        }

    def test_follow_delete_user_is_not_follower(self, api_client, new_user, new_author):
        """
        Follow serializers test
        """
        url = "/api/v1/unsubscribe/"
        api_client.force_authenticate(user=new_user)
        response = api_client.delete(
            url, data={"author": new_author.username}, format="json"
        )
        assert response.status_code == 404
