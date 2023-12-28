import pytest
from django.db import IntegrityError

from src.apps.follow.models import Follow
from src.apps.users.models import CustomUser


@pytest.mark.follow
@pytest.mark.models
def test_follow_fields(django_user_model):
    usernames = ["u1", "u2"]
    users_list = []
    for u in usernames:
        user = django_user_model.objects.create_user(
            username=u, password=f"{u}_password", email=f"{u}@ya.ru"
        )
        users_list.append(user)
    new_follow = Follow.objects.create(user=users_list[0], author=users_list[1])
    # test str
    assert str(new_follow) == f"{usernames[0]} подписан на {usernames[1]}"


@pytest.mark.follow
@pytest.mark.models
def test_follow_twice(django_user_model):
    """
    Can't follow the same user twice
    """
    usernames = ["u1", "u2"]
    users_list = []
    for u in usernames:
        user = django_user_model.objects.create_user(
            username=u, password=f"{u}_password", email=f"{u}@ya.ru"
        )
        users_list.append(user)

    Follow.objects.create(user=users_list[0], author=users_list[1])
    with pytest.raises(IntegrityError):
        Follow.objects.create(user=users_list[0], author=users_list[1])


@pytest.mark.follow
@pytest.mark.models
def test_follow_self(django_user_model):
    """
    User can't follow himself
    """
    u = "u1"
    user = CustomUser.objects.create_user(
        username=u, password=f"{u}_password", email=f"{u}@ya.ru"
    )
    with pytest.raises(IntegrityError):
        f = Follow.objects.create(user=user, author=user)
