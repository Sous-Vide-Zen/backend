from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, AbstractUser
from django.utils import timezone

class CustomUser(AbstractUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(max_length=150, unique=True)
    join_date = models.DateTimeField(default=timezone.now)
    country = models.CharField(max_length=30, blank=True)
    city = models.CharField(max_length=30, blank=True)
    first_name = models.CharField(max_length=30, blank=True)
    second_name = models.CharField(max_length=30, blank=True)
    bio = models.CharField(max_length=200, blank=True)
    avatar = models.ImageField(upload_to='avatars/', max_length=512, blank=True, null=True)
    is_banned = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)


    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

