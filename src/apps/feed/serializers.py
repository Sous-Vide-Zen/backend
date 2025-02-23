from rest_framework.serializers import IntegerField, SerializerMethodField

from src.apps.recipes.serializers import BaseRecipeListSerializer, CategorySerializer


class FeedSerializer(BaseRecipeListSerializer):
    """
    Reflection of Feed page with count of emojies by type in reactions field
    """

    activity_count = IntegerField()
    category = CategorySerializer(many=True, required=False)
    is_favorite = SerializerMethodField()
    reposts_count = IntegerField()

    class Meta(BaseRecipeListSerializer.Meta):
        fields = BaseRecipeListSerializer.Meta.fields + (
            "category",
            "activity_count",
            "is_favorite",
            "reposts_count",
        )

    def get_is_favorite(self, instance):
        user = self.context.get("request").user
        return any(
            favorite.author == user for favorite in getattr(instance, "user_favorites")
        )
