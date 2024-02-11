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
        assert response.data["results"][0]["subscribers_count"] == 0
