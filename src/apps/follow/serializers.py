from rest_framework import serializers

from src.apps.follow.models import Follow
from src.apps.users.models import CustomUser


class UserFollowerSerializer(serializers.ModelSerializer):
    bio = serializers.SerializerMethodField()

    def get_bio(self, obj):
        bio = obj.bio[:50]
        return f"{bio} ..." if bio[-1] == " " else f"{bio}..."

    class Meta:
        model = CustomUser
        fields = ("id", "username", "avatar", "bio")


class FollowListSerializer(serializers.ModelSerializer):
    user = UserFollowerSerializer()
    subscribers_count = serializers.IntegerField()

    class Meta:
        model = Follow
        fields = ("user", "subscribers_count")


