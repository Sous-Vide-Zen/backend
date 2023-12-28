import pytest
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import IntegrityError
from django.utils import timezone

from src.apps.users.models import CustomUser


@pytest.mark.django_db
class TestCustomUserModel:
    def test_user_creation(self, new_user):
        user = new_user
        assert user.email == "test@ya.ru"
        assert user.username == "test"
        assert user.check_password("changeme123")
        assert user.is_authenticated

    def test_user_status(self, new_user):
        user = new_user
        assert user.is_active is True
        assert user.is_banned is False

        user.is_active = False
        user.is_banned = True
        user.save()

        updated_user = CustomUser.objects.get(email="test@ya.ru")
        assert updated_user.is_active is False
        assert updated_user.is_banned is True

    def test_email_uniqueness(self, django_user_model, new_user):
        with pytest.raises(IntegrityError):
            django_user_model.objects.create_user(
                email="test@ya.ru", username="test", password="testpass123"
            )

    def test_is_authenticated_property(self, new_user):
        user = new_user
        assert user.is_authenticated

    def test_avatar_validation(self, new_user):
        with pytest.raises(ValidationError):
            invalid_avatar = SimpleUploadedFile(
                "test_image.bmp", b"file_content", content_type="image/bmp"
            )
            new_user.avatar = invalid_avatar
            new_user.full_clean()

    # Тест на проверку сохранения аватара в правильный путь
    def test_avatar_upload_path(self, new_user):
        user = new_user
        user.avatar = SimpleUploadedFile(
            name="test_avatar.jpg",
            content=b"test_image_content",
            content_type="image/jpeg",
        )
        user.save()
        assert user.avatar.name.startswith(f"avatar/user_{user.id}/")

    # Тест на проверку бана пользователя
    def test_user_ban(self, new_user):
        user = new_user
        assert not user.is_banned
        user.is_banned = True
        user.save()
        assert user.is_banned

    # Тест на проверку активности пользователя
    def test_user_active(self, new_user):
        user = new_user
        user.is_active = False
        assert not user.is_active
        user.is_active = True
        user.save()
        assert user.is_active

    def test_join_date(self, new_user):
        user = new_user
        now = timezone.now()
        assert user.join_date <= now
        assert user.join_date is not None

    def test_name_fields(self, new_user):
        user = CustomUser.objects.create_user(
            "testuser",
            "test@example.com",
            "password123",
            first_name="John",
            second_name="Doe",
        )
        assert user.first_name == "John"
        assert user.second_name == "Doe"

    def test_string_representation(self, new_user):
        user = new_user
        assert str(user) == "test"
