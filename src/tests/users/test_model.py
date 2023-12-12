import pytest
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import IntegrityError
from django.utils import timezone
from src.apps.users.models import CustomUser


@pytest.mark.django_db  # Use this decorator to access the database
class TestCustomUserModel:
    def test_user_creation(self):
        user = CustomUser.objects.create_user(
            username="testuser", email="test@example.com", password="testpassword123"
        )
        assert user.email == "test@example.com"
        assert user.username == "testuser"
        assert user.is_authenticated

    def test_user_status(self):
        user = CustomUser.objects.create_user(
            "testuser", "test@example.com", "password123"
        )
        assert user.is_active is True
        assert user.is_banned is False

        user.is_active = False
        user.is_banned = True
        user.save()

        updated_user = CustomUser.objects.get(email="test@example.com")
        assert updated_user.is_active is False
        assert updated_user.is_banned is True

    def test_unique_email(self):
        CustomUser.objects.create_user("testuser1", "test@example.com", "password123")
        with pytest.raises(IntegrityError):
            CustomUser.objects.create_user(
                "testuser2", "test@example.com", "password123"
            )

    def test_email_uniqueness(self):
        CustomUser.objects.create_user(email="test@example.com", username="testuser1")
        with pytest.raises(IntegrityError):
            CustomUser.objects.create_user(
                email="test@example.com", username="testuser2"
            )

    def test_default_values(self):
        user = CustomUser.objects.create_user(
            email="test@example.com", username="testuser"
        )
        assert user.is_active
        assert not user.is_banned
        # Test other default values similarly

    def test_string_representation(self):
        user = CustomUser.objects.create_user(
            email="test@example.com", username="testuser"
        )
        assert str(user) == "testuser"

    def test_is_authenticated_property(self):
        user = CustomUser.objects.create_user(
            email="test@example.com", username="testuser"
        )
        assert user.is_authenticated  # Note: 'is_authenticated' appears to be a typo

    # Add more tests for other aspects of your model as needed

    def test_avatar_validation(self):
        avatar = SimpleUploadedFile(
            "test_image.jpg", b"file_content", content_type="image/jpeg"
        )
        user = CustomUser.objects.create_user(
            "testuser", "test@example.com", "password123", avatar=avatar
        )
        assert (
            user.avatar.name.endswith(".jpg")
            or user.avatar.name.endswith(".jpeg")
            or user.avatar.name.endswith(".png")
        )

        with pytest.raises(ValidationError):
            invalid_avatar = SimpleUploadedFile(
                "test_image.bmp", b"file_content", content_type="image/bmp"
            )
            user.avatar = invalid_avatar
            user.full_clean()

    # Тест на размер загруженного аватара
    # def test_avatar_size_validation(self):
    #     small_image = SimpleUploadedFile(
    #         name="small_image.jpg",
    #         content=b"small_file_content",
    #         content_type="image/jpeg",
    #     )
    #     large_image = SimpleUploadedFile(
    #         name="large_image.jpg",
    #         content=b"large_file_content"
    #         * 1024
    #         * 1024,  # Большой размер файла для теста
    #         content_type="image/jpeg",
    #     )
    #
    #     # Создаем пользователя с маленьким изображением, ожидаем, что тест пройдет
    #     user_with_small_avatar = CustomUser.objects.create_user(
    #         email="small_avatar@example.com",
    #         username="smallavataruser",
    #         avatar=small_image,
    #     )
    #     try:
    #         user_with_small_avatar.full_clean()
    #     except ValidationError:
    #         pytest.fail("Small avatar should be valid")
    #
    #     # Создаем пользователя с большим изображением, ожидаем ошибку валидации
    #     user_with_large_avatar = CustomUser.objects.create_user(
    #         email="large_avatar@example.com",
    #         username="largeavataruser",
    #         avatar=large_image,
    #     )
    #     with pytest.raises(ValidationError):
    #         user_with_large_avatar.full_clean()

    # Тест на проверку сохранения аватара в правильный путь
    def test_avatar_upload_path(self):
        user = CustomUser.objects.create_user(
            email="test3@example.com", username="testuser3"
        )
        user.avatar = SimpleUploadedFile(
            name="test_avatar.jpg",
            content=b"test_image_content",
            content_type="image/jpeg",
        )
        user.save()
        assert user.avatar.name.startswith(f"avatar/user_{user.id}/")

    # Тест на проверку бана пользователя
    def test_user_ban(self):
        user = CustomUser.objects.create_user(
            email="test4@example.com", username="testuser4"
        )
        assert not user.is_banned
        user.is_banned = True
        user.save()
        assert user.is_banned

    # Тест на проверку активности пользователя
    def test_user_active(self):
        user = CustomUser.objects.create_user(
            email="test5@example.com", username="testuser5", is_active=False
        )
        assert not user.is_active
        user.is_active = True
        user.save()
        assert user.is_active

    def test_join_date(self):
        user = CustomUser.objects.create_user(
            "testuser", "test@example.com", "password123"
        )
        now = timezone.now()
        assert user.join_date <= now
        assert user.join_date is not None

    def test_name_fields(self):
        user = CustomUser.objects.create_user(
            "testuser",
            "test@example.com",
            "password123",
            first_name="John",
            second_name="Doe",
        )
        assert user.first_name == "John"
        assert user.second_name == "Doe"

    def test_string_representation(self):
        user = CustomUser.objects.create_user(
            "testuser", "test@example.com", "password123"
        )
        assert str(user) == "testuser"
