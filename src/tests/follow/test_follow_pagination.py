import pytest
from django.conf import settings

from src.apps.follow.models import Follow
from src.apps.users.models import CustomUser


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
        for i in range(subscriptions_num):
            user = CustomUser.objects.create_user(
                username=f"test_user_{i}",
                email=f"test_user_{i}@x.com",
                password="test_password",
            )
            Follow.objects.create(user=new_user, author=user)
        print(subscriptions_num)

        next_page_url = f"/api/v1/user/{new_user}/subscriptions/"
        api_client.force_authenticate(user=new_user)
        subscriptions_seen, subscriptions_to_see = 0, subscriptions_num

        while subscriptions_seen < TestFollowPagination.page_size * (
            subscriptions_num // TestFollowPagination.page_size
        ):
            response = api_client.get(next_page_url)
            num_subscriptions = len(response.data["results"])
            subscriptions_seen += num_subscriptions
            subscriptions_to_see -= num_subscriptions
            assert num_subscriptions == TestFollowPagination.page_size
            next_page_url = response.data["next"]

        # last page
        if subscriptions_to_see > 0:
            response = api_client.get(next_page_url)
            assert len(response.data["results"]) == subscriptions_to_see
