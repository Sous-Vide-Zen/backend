from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.core.validators import FileExtensionValidator, RegexValidator
from django.db.models import (
    Max,
    CharField,
    EmailField,
    BooleanField,
    ImageField,
    Q,
    CheckConstraint,
    UniqueConstraint,
)
from django.db.transaction import atomic
from phonenumber_field.modelfields import PhoneNumberField

from src.base.services import validate_avatar_size, user_avatar_path, generate_username


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    """

    def create_user(self, email, username=None, password=None, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        with atomic():
            email = self.normalize_email(email)

            max_id = CustomUser.objects.aggregate(Max("id"))["id__max"] or 0
            username_postfix = max_id + 1
            username = generate_username(username_postfix, CustomUser)

            user = self.model(email=email, username=username, **extra_fields)
            user.set_password(password)
            user.save(using=self._db)
            return user

    def create_superuser(self, email, username=None, password=None, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """

        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, username, password, **extra_fields)


class CustomUser(AbstractUser, PermissionsMixin):
    """
    Custom user model.
    """

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    username = CharField(max_length=50, unique=True, blank=True, null=True)
    email = EmailField(max_length=150, unique=True)
    display_name = CharField(max_length=30, blank=True, null=True)
    phone = PhoneNumberField(blank=True, null=True)
    country = CharField(
        max_length=30,
        blank=True,
        null=True,
        default=None,
        validators=[RegexValidator(settings.REGEX)],
    )
    city = CharField(
        max_length=30,
        blank=True,
        null=True,
        default=None,
        validators=[RegexValidator(settings.REGEX)],
    )
    first_name = CharField(
        max_length=30,
        blank=True,
        null=True,
        default=None,
        validators=[RegexValidator(settings.REGEX)],
    )
    last_name = CharField(
        max_length=30,
        blank=True,
        null=True,
        default=None,
        validators=[RegexValidator(settings.REGEX)],
    )
    bio = CharField(max_length=200, blank=True, null=True, default=None)
    avatar = ImageField(
        upload_to=user_avatar_path,
        blank=True,
        null=True,
        validators=[
            validate_avatar_size,
            FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png"]),
        ],
    )
    is_banned = BooleanField(default=False)
    is_active = BooleanField(default=True)
    is_staff = BooleanField(default=False)
    is_admin = BooleanField(default=False)

    class Meta:
        """
        Meta class for CustomUser model
        """

        verbose_name = "user"
        verbose_name_plural = "users"
        ordering = ["-date_joined"]
        constraints = [
            UniqueConstraint(fields=["email"], name="unique_email"),
            CheckConstraint(check=~Q(username="me"), name="not_me"),
        ]

    @property
    def is_autenticated(self):
        """
        This method is used to check if user is authenticated or not
        """

        return True

    def __str__(self):
        """
        This method is used to return username of the user
        """

        return self.username
