from rest_framework import serializers
from .models import CustomUser


class CustomUserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "username",
            "email",
            "join_date",
            "country",
            "city",
            "first_name",
            "second_name",
            "bio",
            "is_active",
            "is_staff",
            "is_admin",
        ]


class CustomUserMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "username", "avatar", "is_active", "is_staff", "is_admin"]
