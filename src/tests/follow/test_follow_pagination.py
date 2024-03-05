import factory
import pytest
from django.conf import settings
from factory.django import DjangoModelFactory

from src.apps.follow.models import Follow
from src.apps.users.models import CustomUser


class CustomUserFactory(DjangoModelFactory):
    class Meta:
        model = CustomUser

    username = factory.Sequence(lambda n: f"test_user_{n}")
    email = factory.LazyAttribute(lambda o: f"{o.username}@x.com")
    password = "test_password"


class FollowFactory(DjangoModelFactory):
    class Meta:
        model = Follow

    user = factory.SubFactory(CustomUserFactory)
    author = factory.SubFactory(CustomUserFactory)


@pytest.mark.django_db
@pytest.mark.api
class TestFollowPagination:
    page_size = settings.FOLLOWER_PAGE_SIZE

    @pytest.mark.parametrize(
        "subscriptions_num",
        list(range(page_size, page_size * 3, 3)),
    )
    def test_follow_pagination(self, api_client, new_user, subscriptions_num):
        """
        Follow pagination test
        """
        FollowFactory.create_batch(subscriptions_num, user=new_user)

        next_page_url = f"/api/v1/user/{new_user}/subscriptions/"
        api_client.force_authenticate(user=new_user)
        while next_page_url:
            response = api_client.get(next_page_url)
            num_subscriptions = len(response.data["results"])
            assert num_subscriptions == min(
                TestFollowPagination.page_size, subscriptions_num
            )
            next_page_url = response.data["next"]
            subscriptions_num -= TestFollowPagination.page_size
