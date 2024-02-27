from django.conf import settings
from rest_framework import serializers

from src.apps.follow.models import Follow
from src.apps.users.models import CustomUser


class UserFollowerSerializer(serializers.ModelSerializer):
    bio = serializers.SerializerMethodField()

    def get_bio(self, obj):
        if obj.bio:
            bio = obj.bio[: settings.SHORT_BIO_SYMBOLS]
            return f"{bio} ..." if bio[-1] == " " else f"{bio}..."

    class Meta:
        model = CustomUser
        fields = ("id", "username", "avatar", "bio")


class FollowListSerializer(serializers.ModelSerializer):
    author = UserFollowerSerializer()
    subscribers_count = serializers.IntegerField()

    class Meta:
        model = Follow
        fields = (
            "id",
            "author",
            "subscribers_count",
        )


class FollowerListSerializer(serializers.ModelSerializer):
    user = UserFollowerSerializer()
    subscribers_count = serializers.IntegerField()

    class Meta:
        model = Follow
        fields = ("id", "user", "subscribers_count")


class FollowCreateSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username", queryset=CustomUser.objects.all()
    )
    user = serializers.SlugRelatedField(
        slug_field="username",
        queryset=CustomUser.objects.all(),
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        fields = (
            "author",
            "user",
            "created_at",
        )
        model = Follow
        extra_kwargs = {"created_at": {"read_only": True}}

    def validate(self, data):
        user = self.context["request"].user
        author = data.get("author")

        if not author:
            raise serializers.ValidationError({"message": "Отсутствует автор"})

        if user == author:
            raise serializers.ValidationError("Нельзя подписаться на самого себя.")

        queryset = Follow.objects.filter(user=user, author=author)
        if queryset.count() > 0:
            raise serializers.ValidationError(
                {"message": "Вы уже подписаны на этого автора"}
            )

        return data
