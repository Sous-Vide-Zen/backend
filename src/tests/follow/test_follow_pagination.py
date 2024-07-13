import pytest
from django.conf import settings

from tests.factories.factories import FollowFactory


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
