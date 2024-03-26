from rest_framework.routers import DefaultRouter

from src.apps.reactions.views import RecipeReactionViewSet, CommentReactionViewSet

router = DefaultRouter()
router.register(
    r"recipe/(?P<slug>[^/.]+)/reactions",
    RecipeReactionViewSet,
    basename="recipe-reactions",
)
router.register(
    r"comment/(?P<id>\d+)/reactions",
    CommentReactionViewSet,
    basename="comment-reactions",
)

urlpatterns = router.urls
