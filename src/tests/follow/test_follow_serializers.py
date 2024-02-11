import pytest
from django.db.utils import IntegrityError

from src.apps.follow.models import Follow
from src.apps.follow.serializers import UserFollowerSerializer
from src.apps.users.models import CustomUser


@pytest.mark.django_db
def test_follow_serializer():
    """
    Follow serializer test for create method with valid data and with invalid data for user and author
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
    assert follow.author == user2


@pytest.mark.django_db
def test_follow_serializer_with_invalid_data():
    """
    Follow serializer test for create method with invalid data for user and author
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

    with pytest.raises(IntegrityError):
        Follow.objects.create(user=user, author=user2)
        Follow.objects.create(user=user, author=user)


@pytest.mark.django_db
def test_user_follower_serializer():
    """
    User follower serializer test for get method
    """
    user = CustomUser.objects.create_user(
        username="test_user",
        email="test_user@x.com",
        password="test_password",
        bio="short bio example",
    )
    user2 = CustomUser.objects.create_user(
        username="test_user2",
        email="test_user2@x.com",
        password="test_password",
        bio="long bio example",
    )

    follow = Follow.objects.create(user=user, author=user2)

    serializer = UserFollowerSerializer(follow.author)
    assert serializer.data == {
        "id": user2.pk,
        "username": user2.username,
        "avatar": user2.avatar,
        "bio": "long bio example...",
    }


# @pytest.mark.django_db
# def test_follow_list_serializer():
#     """
#     Follow list serializer test for get method
#     """
#     user = CustomUser.objects.create_user(
#         username="test_user",
#         email="test_user@x.com",
#         password="test_password",
#     )
#     user2 = CustomUser.objects.create_user(
#         username="test_user2",
#         email="test_user2@x.com",
#         password="test_password",
#     )
#     user3 = CustomUser.objects.create_user(
#         username="test_user3",
#         email="test_user3@x.com",
#         password="test_password",
#     )
#
#     serializer = FollowListSerializer(Follow.objects.all(), many=True)
#     assert serializer.data == [
#         {
#             "id": Follow.objects.get(user=user, author=user2).pk,
#             "author": {
#                 "id": user2.pk,
#                 "username": user2.username,
#                 "avatar": user2.avatar,
#                 "bio": "",
#             },
#         },
#         {
#             "id": Follow.objects.get(user=user, author=user3).pk,
#             "author": {
#                 "id": user3.pk,
#                 "username": user3.username,
#                 "avatar": user3.avatar,
#                 "bio": "",
#             },
#         },
#     ]
