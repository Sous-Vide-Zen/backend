from backend.src.base.services import validate_avatar_size, user_avatar_path
from django.db import models
from django.utils import timezone


class CustomUser(models.Model):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(max_length=150, unique=True)
    join_date = models.DateTimeField(default=timezone.now)
    country = models.CharField(max_length=30, blank=True)
    city = models.CharField(max_length=30, blank=True)
    first_name = models.CharField(max_length=30, blank=True)
    second_name = models.CharField(max_length=30, blank=True)
    bio = models.CharField(max_length=200, blank=True)
    avatar = models.ImageField(upload_to=user_avatar_path, blank=True, null=True, validators=[validate_avatar_size])
    is_banned = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email
