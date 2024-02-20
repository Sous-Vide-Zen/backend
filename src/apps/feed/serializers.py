from rest_framework import serializers
from taggit.serializers import TagListSerializerField

from src.apps.reactions.models import Reaction
from src.apps.recipes.models import Recipe
from src.apps.users.models import CustomUser


class ReactionSerializer(serializers.ModelSerializer):
    # не используется в связи с тем, что в поле "reactions"
    # указывается общее кол-во emoji по типам

    class Meta:
        model = Reaction
        fields = ["author", "pub_date", "emoji"]


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "username", "avatar"]


class FeedSerializer(serializers.ModelSerializer):
    total_comments_count = serializers.IntegerField()
    total_views_count = serializers.IntegerField()
    total_reactions_count = serializers.IntegerField()
    # reactions = ReactionSerializer(many=True, read_only=True)
    tag = TagListSerializerField()
    author = AuthorSerializer()
    activity_count = serializers.IntegerField()
    reactions = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = [
            "id",
            "title",
            "slug",
            "category",
            "short_text",
            "preview_image",
            "author",
            "pub_date",
            "tag",
            "cooking_time",
            "total_comments_count",
            "total_views_count",
            "total_reactions_count",
            "reactions",
            "activity_count",
        ]

    def get_reactions(self, obj):
        reactions = obj.reactions.all()
        emotions = dict()
        for reaction in reactions:
            emotions[reaction.emoji] = reactions.filter(emoji=reaction.emoji).count()
        return emotions
