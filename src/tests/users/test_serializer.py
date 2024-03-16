import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone

from src.apps.users.serializers import (
    UserListSerializer,
    CustomUserSerializer,
    CustomUserMeSerializer,
    AuthorInRecipeSerializer,
)


@pytest.fixture
def user(db):
    User = get_user_model()
    user = User.objects.create_user(
        username="testuser",
        display_name="Test User",
        email="test@example.com",
        avatar="path/to/avatar.png",
        phone="1234567890",
        password="123xXXXXXXXXX!",
        date_joined=timezone.now(),
        country="Testland",
        city="Testville",
        first_name="Test",
        last_name="User",
        bio="This is a test user.",
        is_active=True,
        is_staff=False,
        is_admin=False,
    )
    return user


@pytest.mark.django_db
class TestUserSerializer:
    @pytest.mark.api
    def test_user_list_serializer(self, user):
        user.is_follow = False
        user.is_follower = True
        user.recipes_count = 5

        serializer = UserListSerializer(instance=user)
        data = serializer.data

        assert data["username"] == user.username
        assert data["display_name"] == user.display_name
        assert data["avatar"] == user.avatar.url
        assert data["is_follow"] == user.is_follow
        assert data["is_follower"] == user.is_follower
        assert data["recipes_count"] == 5

    @pytest.mark.api
    def test_custom_user_serializer(self, user):
        serializer = CustomUserSerializer(instance=user)
        data = serializer.data

        assert data["username"] == user.username
        assert data["display_name"] == user.display_name
        assert data["email"] == user.email
        assert data["avatar"] == user.avatar.url
        assert data["phone"] == user.phone
        assert data["date_joined"] == user.date_joined.isoformat().replace(
            "+00:00", "Z"
        )
        assert data["country"] == user.country
        assert data["city"] == user.city
        assert data["first_name"] == user.first_name
        assert data["last_name"] == user.last_name
        assert data["bio"] == user.bio
        assert data["is_active"] == user.is_active
        assert data["is_staff"] == user.is_staff
        assert data["is_admin"] == user.is_admin

    @pytest.mark.api
    def test_custom_user_me_serializer(self, user):
        serializer = CustomUserMeSerializer(instance=user)
        data = serializer.data

        assert data["username"] == user.username
        assert data["display_name"] == user.display_name
        assert data["avatar"] == user.avatar.url
        assert data["is_active"] == user.is_active
        assert data["is_staff"] == user.is_staff
        assert data["is_admin"] == user.is_admin

    @pytest.mark.api
    def test_author_in_recipe_serializer(self, user):
        serializer = AuthorInRecipeSerializer(instance=user)
        data = serializer.data

        assert data["username"] == user.username
        assert data["display_name"] == user.display_name
        assert data["avatar"] == user.avatar.url
