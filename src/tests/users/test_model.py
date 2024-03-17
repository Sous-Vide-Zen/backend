import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import IntegrityError
from django.utils import timezone

from src.apps.users.emails import CustomActivationEmail
from src.apps.users.models import CustomUser


@pytest.mark.django_db
class TestCustomUserModel:
    """
    Test CustomUser model
    """

    def test_user_creation(self, new_user):
        """
        Test user creation
        """

        user = new_user
        assert user.email == "test@ya.ru"
        assert user.username == "user1"
        assert user.check_password("changeme123")
        assert user.is_authenticated

    def test_user_status(self, new_user):
        """
        Test user status
        """

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
        """
        Test email uniqueness
        """

        with pytest.raises(IntegrityError):
            django_user_model.objects.create_user(
                email="test@ya.ru", username="test", password="testpass123"
            )

    def test_is_authenticated_property(self, new_user):
        """
        Test is_authenticated property
        """

        assert new_user.is_autenticated

    def test_avatar_validation(self, new_user):
        """
        Test avatar validation
        """

        with pytest.raises(ValidationError):
            invalid_avatar = SimpleUploadedFile(
                "test_image.bmp", b"file_content", content_type="image/bmp"
            )
            new_user.avatar = invalid_avatar
            new_user.full_clean()

    # Тест на проверку сохранения аватара в правильный путь
    def test_avatar_upload_path(self, new_user):
        """
        Test avatar upload path
        """

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
        """
        Test user ban
        """

        user = new_user
        assert not user.is_banned
        user.is_banned = True
        user.save()
        assert user.is_banned

    # Тест на проверку активности пользователя
    def test_user_active(self, new_user):
        """
        Test user active
        """

        user = new_user
        user.is_active = False
        assert not user.is_active
        user.is_active = True
        user.save()
        assert user.is_active

    def test_join_date(self, new_user):
        """
        Test join date
        """

        user = new_user
        now = timezone.now()
        assert user.date_joined <= now
        assert user.date_joined is not None

    def test_name_fields(self, new_user):
        """
        Test name fields
        """

        user = CustomUser.objects.create_user(
            "testuser",
            "test@example.com",
            "password123",
            first_name="John",
            last_name="Doe",
        )
        assert user.first_name == "John"
        assert user.last_name == "Doe"

    def test_string_representation(self, new_user):
        """
        Test string representation
        """

        user = new_user
        assert str(user) == "user1"

    def test_create_superuser(self):
        """
        Test create superuser
        """

        user = get_user_model().objects.create_superuser(
            email="test@ya.ru", username="test", password="testpass123"
        )
        assert user.is_superuser
        assert user.is_staff
        assert user.is_active
        assert user.is_admin


@pytest.mark.django_db
class TestCustomActivationEmail:
    """
    Test CustomActivationEmail
    """

    def test_template_name(self):
        """
        Test template_name
        """

        assert CustomActivationEmail.template_name == "activation.html"
