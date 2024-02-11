import pytest

from src.apps.follow.models import Follow
from src.apps.users.models import CustomUser


@pytest.mark.django_db
def test_follow_url(api_client):
    """
    Follow url test
    """
    user = CustomUser.objects.create_user(
        username="test_user",
        email="test_user@x.com",
        password="test_password",
    )
    user2 = CustomUser.objects.create_user(
        username="test_user2",
        email="test_user2@x.com",
        password="test_password",
    )

    follow = Follow.objects.create(user=user, author=user2)

    url = f"/api/v1/user/{user2}/subscriptions/"
    print(url)
    response = api_client.get(url)
    assert response.status_code == 200
