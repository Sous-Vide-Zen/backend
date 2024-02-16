from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField


from src.base.services import validate_avatar_size, user_avatar_path


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username=None, password=None, **extra_fields):
        # if not email:
        #     raise ValueError('The Email field must be set')
        email = self.normalize_email(email)

        if username is None:  # Если username не указан, установите его в None
            username = None

        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, username, password, **extra_fields)


class CustomUser(AbstractUser, PermissionsMixin):

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    username = models.CharField(max_length=50, unique=True, blank=True, null=True)
    email = models.EmailField(max_length=150, unique=True)
    phone = PhoneNumberField(blank=True, null=True)
    join_date = models.DateTimeField(default=timezone.now)
    country = models.CharField(max_length=30, blank=True, null=True, default=None)
    city = models.CharField(max_length=30, blank=True, null=True, default=None)
    first_name = models.CharField(max_length=30, blank=True, null=True, default=None)
    last_name = models.CharField(max_length=30, blank=True, null=True, default=None)
    bio = models.CharField(max_length=200, blank=True, null=True, default=None)
    avatar = models.ImageField(
        upload_to=user_avatar_path,
        blank=True,
        null=True,
        validators=[
            validate_avatar_size,
            FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png"]),
        ],
    )
    is_banned = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super().save(
            *args, **kwargs
        )  # сначала сохраняем пользователя, чтобы получить id
        if not self.username:  # если username не задан
            new_username = f"user{self.id}"  # устанавливаем username равным user+id
            while CustomUser.objects.filter(
                username=new_username
            ).exists():  # проверяем, существует ли уже такой username
                new_username += (
                    "1"  # если существует, добавляем к username дополнительные символы
                )
            self.username = new_username
            super().save(update_fields=["username"])

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
        ordering = ["-join_date"]
        constraints = [
            models.UniqueConstraint(fields=["email"], name="unique_email"),
            models.CheckConstraint(check=~models.Q(username="me"), name="not_me"),
        ]

    @property
    def is_autenticated(self):
        return True

    def __str__(self):
        return self.username
