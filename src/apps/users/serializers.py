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

    def validate_username(self, value):
        """
        Проверка уникальности username.
        """
        user_model = get_user_model()
        username_exists = (
            user_model.objects.filter(username=value)
            .exclude(id=self.instance.id)
            .exists()
        )

        if username_exists:
            raise serializers.ValidationError(
                "A user with that username already exists."
            )
        return value


class CustomUserMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "username", "avatar", "is_active", "is_staff", "is_admin"]
