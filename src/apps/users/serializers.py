from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "username",
            "email",
            "avatar",
            "phone",
            "join_date",
            "country",
            "city",
            "first_name",
            "last_name",
            "bio",
            "is_active",
            "is_staff",
            "is_admin",
        ]


class CustomUserMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "username", "avatar", "is_active", "is_staff", "is_admin"]


class AuthorInRecipeSerializer(serializers.ModelSerializer):
    """
    Author in recipe serializer
    """

    class Meta:
        model = CustomUser
        fields = ("id", "username", "display_name", "avatar")
