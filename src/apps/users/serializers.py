from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializer for CustomUser model
    """

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


class UserListSerializer(serializers.ModelSerializer):
    """
    Serializer for CustomUser model for list endpoint
    """

    is_follow = serializers.BooleanField()
    is_follower = serializers.BooleanField()
    recipes_count = serializers.IntegerField()

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "username",
            "avatar",
            "recipes_count",
            "is_follow",
            "is_follower",
        )


class CustomUserMeSerializer(serializers.ModelSerializer):
    """
    Serializer for CustomUser model for me endpoint
    """

    class Meta:
        model = CustomUser
        fields = ("id", "username", "avatar", "is_active", "is_staff", "is_admin")
